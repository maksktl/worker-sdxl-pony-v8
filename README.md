<div align="center">

<h1>Anime/Hentai NSFW Worker</h1>

🚀 | RunPod Serverless worker for high-quality anime/hentai image generation.  
Based on NTR Mix Illustrious XL v4.0 model.
</div>

## Features

- **NTR Mix Illustrious XL v4.0** - High-quality anime/hentai model
- **SDXL VAE** - Prevents washed-out colors
- **Optimized settings** - Euler a scheduler, CFG 5.5, quality tags
- **Illustrious-based** - Best for anime art style

---

## 📥 Required Model Files

**Before building the Docker image, you must download and place these files in the `models/` directory:**

### 1. Checkpoint Model (models/checkpoints/)

| File | Source | Size |
|------|--------|------|
| `ntrMIXIllustriousXL_v40.safetensors` | [CivitAI](https://civitai.com/models/926443?modelVersionId=1061268) | ~6.5 GB |

### 2. VAE (models/vae/)

| File | Source | Size |
|------|--------|------|
| `sdxl_vae.safetensors` | [HuggingFace](https://huggingface.co/stabilityai/sdxl-vae/blob/main/sdxl_vae.safetensors) | ~335 MB |

---

## 📁 Final Directory Structure

```
models/
├── checkpoints/
│   └── ntrMIXIllustriousXL_v40.safetensors
└── vae/
    └── sdxl_vae.safetensors
```

---

## 🚀 Building & Deploying

```bash
# Build Docker image
docker build -t anime-nsfw-worker .

# Push to your registry
docker tag anime-nsfw-worker your-registry/anime-nsfw-worker:latest
docker push your-registry/anime-nsfw-worker:latest
```

---

## 📝 API Usage

### Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | **required** | Your image description (anime tags) |
| `negative_prompt` | string | (quality defaults) | What to avoid |
| `width` | int | 832 | Image width |
| `height` | int | 1216 | Image height |
| `num_inference_steps` | int | 28 | Generation steps |
| `guidance_scale` | float | 5.5 | CFG scale (lower for Illustrious) |
| `seed` | int | random | Reproducibility seed |
| `scheduler` | string | "Euler a" | Sampling method |
| `num_images` | int | 1 | Images to generate (1-3) |
| `add_quality_tags` | bool | true | Add "masterpiece, best quality..." prefix |

### Example Request

```json
{
  "input": {
    "prompt": "1girl, nude, breasts, black hair, large breasts, long hair, blush, looking at viewer, bedroom",
    "width": 832,
    "height": 1216,
    "num_inference_steps": 28,
    "guidance_scale": 5.5
  }
}
```

### Response

```json
{
  "images": ["data:image/png;base64,..."],
  "image_url": "data:image/png;base64,...",
  "seed": 123456789,
  "prompt_used": "masterpiece, best quality, amazing quality, absurdres, highres, 1girl, nude...",
  "negative_prompt_used": "(low quality, worst quality:1.5), (bad anatomy)..."
}
```

---

## 🎨 Recommended Aspect Ratios

| Orientation | Size | Ratio |
|-------------|------|-------|
| Portrait | 832x1216 | 2:3 |
| Landscape | 1216x832 | 3:2 |
| Square | 1024x1024 | 1:1 |

---

## 💡 Prompting Tips for Anime

Use **Danbooru/anime tags** style:
- `1girl`, `1boy`, `solo`, `multiple girls`
- Body: `large breasts`, `small breasts`, `slender`, `thick thighs`
- Hair: `black hair`, `blonde hair`, `long hair`, `twintails`
- Eyes: `blue eyes`, `closed eyes`, `looking at viewer`
- Pose: `standing`, `sitting`, `lying`, `all fours`
- NSFW: `nude`, `nipples`, `sex`, `vaginal`, `missionary`
- Style: `blush`, `sweat`, `open mouth`, `tongue out`

---

## 📚 Credits

- Model: [NTR Mix Illustrious XL](https://civitai.com/models/926443) 
- Base: [Illustrious XL](https://civitai.com/models/795765/illustrious-xl)
- Guide: [BetterWaifu NSFW Tutorial](https://betterwaifu.com/blog/stable-diffusion-nsfw)
