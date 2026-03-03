"""
Input schema for the Anime/Hentai NSFW image generation worker.
Based on WAI-NSFW-illustrious-SDXL v16 model.
"""

# Default negative prompt for WAI-NSFW-illustrious-SDXL v16
DEFAULT_NEGATIVE_PROMPT = (
    "bad quality, worst quality, worst detail, sketch, censor, "
    "lowres, (bad anatomy:1.2), jpeg artifacts, signature, watermark, "
    "old, oldest, censored, bar_censor, extra digits, fewer digits, "
    "extra arms, missing arms, too many fingers, fused fingers, "
    "missing fingers, ugly, blurry"
)

# Quality tags for WAI-NSFW-illustrious-SDXL v16
ILLUSTRIOUS_QUALITY_TAGS = "masterpiece, best quality, amazing quality, very aesthetic, absurdres, newest"

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
        'default': 6.0  # WAI v16 recommended: 5-7
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
