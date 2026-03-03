<div align="center">

<h1>Anime/Hentai NSFW Worker</h1>

🚀 | RunPod Serverless worker for high-quality anime/hentai image generation.  
Based on WAI-NSFW-illustrious-SDXL v16 model.
</div>

## Features

- **WAI-NSFW-illustrious-SDXL v16** - Top-rated anime/hentai model with best character knowledge
- **Built-in VAE** - No separate VAE needed, colors are great out of the box
- **Optimized settings** - Euler a scheduler, CFG 6.0, enhanced quality tags
- **Illustrious-based** - Best for anime art style, NSFW poses, and canonical characters

---

## 📥 Required Model Files

**Before building the Docker image, you must download and place these files in the `models/` directory:**

### 1. Checkpoint Model (models/checkpoints/)

| File | Source | Size |
|------|--------|------|
| `waiNSFWillustriousSDXL_v160.safetensors` | [CivitAI](https://civitai.com/models/827184/wai-illustrious-sdxl) | ~6.46 GB |

> ✅ **VAE is built into the model** — no separate VAE file needed!

---

## 📁 Final Directory Structure

```
models/
└── checkpoints/
    └── waiNSFWillustriousSDXL_v160.safetensors
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
| `guidance_scale` | float | 6.0 | CFG scale (WAI v16 recommended: 5-7) |
| `seed` | int | random | Reproducibility seed |
| `scheduler` | string | "Euler a" | Sampling method |
| `num_images` | int | 1 | Images to generate (1-3) |
| `add_quality_tags` | bool | true | Add "masterpiece, best quality..." prefix |

### Example Request

```json
{
  "input": {
    "prompt": "1girl, nude, breasts, black hair, large breasts, long hair, blush, looking at viewer, bedroom, explicit",
    "width": 832,
    "height": 1216,
    "num_inference_steps": 28,
    "guidance_scale": 6.0
  }
}
```

### Response

```json
{
  "images": ["data:image/png;base64,..."],
  "image_url": "data:image/png;base64,...",
  "seed": 123456789,
  "prompt_used": "masterpiece, best quality, amazing quality, very aesthetic, absurdres, newest, 1girl, nude...",
  "negative_prompt_used": "bad quality, worst quality, worst detail, sketch, censor..."
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

## 💡 Prompting Tips for WAI-NSFW

Use **Danbooru/anime tags** style:
- `1girl`, `1boy`, `solo`, `multiple girls`
- Body: `large breasts`, `small breasts`, `slender`, `thick thighs`
- Hair: `black hair`, `blonde hair`, `long hair`, `twintails`
- Eyes: `blue eyes`, `closed eyes`, `looking at viewer`
- Pose: `standing`, `sitting`, `lying`, `all fours`
- NSFW: `nude`, `nipples`, `sex`, `vaginal`, `missionary`
- Style: `blush`, `sweat`, `open mouth`, `tongue out`
- **Safety tags**: `general`, `sensitive`, `nsfw`, `explicit` (add `explicit` for NSFW content)
- **Characters**: WAI v16 knows most anime/game characters — use their name directly

---

## 📚 Credits

- Model: [WAI-NSFW-illustrious-SDXL v16](https://civitai.com/models/827184/wai-illustrious-sdxl)
- Base: [Illustrious XL](https://civitai.com/models/795765/illustrious-xl)
- Guide: [BetterWaifu NSFW Tutorial](https://betterwaifu.com/blog/stable-diffusion-nsfw)
