"""
Input schema for the Anime/Hentai NSFW image generation worker.
Based on NTR Mix Illustrious XL model.
"""

# Default negative prompt for anime quality (Illustrious-based models)
DEFAULT_NEGATIVE_PROMPT = (
    "(low quality, worst quality:1.5), (bad anatomy), lowres, bad composition, "
    "fewer digits, text, username, logo, inaccurate eyes, extra digits, "
    "extra arms, disfigured, missing arms, too many fingers, fused fingers, "
    "missing fingers, ugly, blurry"
)

# Quality tags for Illustrious models (different from Pony!)
ILLUSTRIOUS_QUALITY_TAGS = "masterpiece, best quality, amazing quality, absurdres, highres"

INPUT_SCHEMA = {
    'prompt': {
        'type': str,
        'required': True,
    },
    'negative_prompt': {
        'type': str,
        'required': False,
        'default': DEFAULT_NEGATIVE_PROMPT
    },
    'height': {
        'type': int,
        'required': False,
        'default': 1216  # Optimal for portrait (832x1216)
    },
    'width': {
        'type': int,
        'required': False,
        'default': 832  # Optimal for portrait
    },
    'seed': {
        'type': int,
        'required': False,
        'default': None
    },
    'scheduler': {
        'type': str,
        'required': False,
        'default': 'Euler a'  # Recommended for Illustrious models
    },
    'num_inference_steps': {
        'type': int,
        'required': False,
        'default': 28  # Recommended by the guide for anime
    },
    'guidance_scale': {
        'type': float,
        'required': False,
        'default': 5.5  # Lower CFG for Illustrious (5-5.5)
    },
    'strength': {
        'type': float,
        'required': False,
        'default': 0.5
    },
    'image_url': {
        'type': str,
        'required': False,
        'default': None
    },
    'num_images': {
        'type': int,
        'required': False,
        'default': 1,
        'constraints': lambda img_count: 4 > img_count > 0
    },
    # Quality tags prefix for Illustrious models
    'add_quality_tags': {
        'type': bool,
        'required': False,
        'default': True  # Adds "masterpiece, best quality, amazing quality..." prefix
    },
}
