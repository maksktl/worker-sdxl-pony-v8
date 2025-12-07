"""
Anime/Hentai NSFW Image Generation Worker for RunPod Serverless.
Based on NTR Mix Illustrious XL model.
"""

import os
import base64

import torch
from diffusers import StableDiffusionXLPipeline, AutoencoderKL
from diffusers.utils import load_image

from diffusers import (
    PNDMScheduler,
    LMSDiscreteScheduler,
    DDIMScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    DPMSolverMultistepScheduler,
)

import runpod
from runpod.serverless.utils import rp_upload, rp_cleanup
from runpod.serverless.utils.rp_validator import validate

from rp_schemas import (
    INPUT_SCHEMA,
    ILLUSTRIOUS_QUALITY_TAGS,
)

torch.cuda.empty_cache()

# --------------------------------- Paths ------------------------------------ #

MODEL_BASE_PATH = "/models"
CHECKPOINT_PATH = os.path.join(MODEL_BASE_PATH, "checkpoints", "ntrMIXIllustriousXL_v40.safetensors")
VAE_PATH = os.path.join(MODEL_BASE_PATH, "vae", "sdxl_vae.safetensors")

# ------------------------------- Model Handler ------------------------------ #


class ModelHandler:
    def __init__(self):
        self.pipe = None
        self.load_models()

    def load_models(self):
        print("Loading NTR Mix Illustrious XL v4.0 checkpoint...")
        
        # Load VAE
        vae = AutoencoderKL.from_single_file(
            VAE_PATH,
            torch_dtype=torch.float16
        )
        
        # Load main pipeline from local checkpoint
        self.pipe = StableDiffusionXLPipeline.from_single_file(
            CHECKPOINT_PATH,
            vae=vae,
            torch_dtype=torch.float16,
            use_safetensors=True,
            add_watermarker=False
        )
        
        self.pipe = self.pipe.to("cuda", silence_dtype_warnings=True)
        self.pipe.enable_xformers_memory_efficient_attention()
        
        print("Model loaded successfully!")


MODELS = ModelHandler()

# ---------------------------------- Helper ---------------------------------- #


def _save_and_upload_images(images, job_id):
    os.makedirs(f"/{job_id}", exist_ok=True)
    image_urls = []
    for index, image in enumerate(images):
        image_path = os.path.join(f"/{job_id}", f"{index}.png")
        image.save(image_path)

        if os.environ.get('BUCKET_ENDPOINT_URL', False):
            image_url = rp_upload.upload_image(job_id, image_path)
            image_urls.append(image_url)
        else:
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(
                    image_file.read()).decode("utf-8")
                image_urls.append(f"data:image/png;base64,{image_data}")

    rp_cleanup.clean([f"/{job_id}"])
    return image_urls


def make_scheduler(name, config):
    """Create scheduler based on name."""
    schedulers = {
        "PNDM": lambda: PNDMScheduler.from_config(config),
        "KLMS": lambda: LMSDiscreteScheduler.from_config(config),
        "DDIM": lambda: DDIMScheduler.from_config(config),
        "K_EULER": lambda: EulerDiscreteScheduler.from_config(config),
        "K_EULER_ANCESTRAL": lambda: EulerAncestralDiscreteScheduler.from_config(config),
        "DPMSolverMultistep": lambda: DPMSolverMultistepScheduler.from_config(config),
        "DPM++ 2M SDE Karras": lambda: DPMSolverMultistepScheduler.from_config(
            config,
            algorithm_type="sde-dpmsolver++",
            use_karras_sigmas=True
        ),
        "DPM++ 2M Karras": lambda: DPMSolverMultistepScheduler.from_config(
            config,
            use_karras_sigmas=True
        ),
        "Euler a": lambda: EulerAncestralDiscreteScheduler.from_config(config),
    }
    
    if name not in schedulers:
        print(f"Unknown scheduler '{name}', using DPM++ 2M SDE Karras")
        name = "DPM++ 2M SDE Karras"
    
    return schedulers[name]()


def build_prompt(base_prompt: str, add_quality_tags: bool) -> str:
    """Build the final prompt with quality tags for Illustrious models."""
    parts = []
    
    # Add Illustrious quality tags (masterpiece, best quality, etc.)
    if add_quality_tags:
        parts.append(ILLUSTRIOUS_QUALITY_TAGS)
    
    # Add user prompt
    parts.append(base_prompt.strip())
    
    return ", ".join(parts)


@torch.inference_mode()
def generate_image(job):
    """Generate an anime/hentai image using NTR Mix Illustrious XL model."""
    job_input = job["input"]

    # Input validation
    validated_input = validate(job_input, INPUT_SCHEMA)

    if 'errors' in validated_input:
        return {"error": validated_input['errors']}
    job_input = validated_input['validated_input']

    starting_image = job_input.get('image_url')

    if job_input['seed'] is None:
        job_input['seed'] = int.from_bytes(os.urandom(4), "big")

    generator = torch.Generator("cuda").manual_seed(job_input['seed'])

    # Set scheduler
    MODELS.pipe.scheduler = make_scheduler(
        job_input['scheduler'], MODELS.pipe.scheduler.config)

    # Build prompts with Illustrious quality tags
    final_prompt = build_prompt(
        job_input['prompt'],
        job_input.get('add_quality_tags', True)
    )
    
    final_negative = job_input.get('negative_prompt', '')

    print(f"Final prompt: {final_prompt}")
    print(f"Final negative: {final_negative}")

    if starting_image:
        init_image = load_image(starting_image).convert("RGB")
        output = MODELS.pipe(
            prompt=final_prompt,
            negative_prompt=final_negative,
            num_inference_steps=job_input['num_inference_steps'],
            strength=job_input['strength'],
            image=init_image,
            guidance_scale=job_input['guidance_scale'],
            generator=generator
        ).images
    else:
        try:
            output = MODELS.pipe(
                prompt=final_prompt,
                negative_prompt=final_negative,
                height=job_input['height'],
                width=job_input['width'],
                num_inference_steps=job_input['num_inference_steps'],
                guidance_scale=job_input['guidance_scale'],
                num_images_per_prompt=job_input['num_images'],
                generator=generator
            ).images
        except RuntimeError as err:
            return {
                "error": f"RuntimeError: {err}, Stack Trace: {err.__traceback__}",
                "refresh_worker": True
            }

    image_urls = _save_and_upload_images(output, job['id'])

    results = {
        "images": image_urls,
        "image_url": image_urls[0],
        "seed": job_input['seed'],
        "prompt_used": final_prompt,
        "negative_prompt_used": final_negative,
    }

    if starting_image:
        results['refresh_worker'] = True

    return results


runpod.serverless.start({"handler": generate_image})
