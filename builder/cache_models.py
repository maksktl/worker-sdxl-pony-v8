# builder/cache_models.py
"""
Downloads model files from Yandex.Disk during Docker build.
Based on WAI-NSFW-illustrious-SDXL v16 for anime/hentai generation.
"""

import os
import sys
import requests

# Model paths configuration
MODEL_BASE_PATH = "/models"
CHECKPOINT_PATH = os.path.join(MODEL_BASE_PATH, "checkpoints")

# ============================================================================
# ВСТАВЬТЕ ВАШИ ССЫЛКИ НА ЯНДЕКС.ДИСК СЮДА:
# ============================================================================

YANDEX_DISK_LINKS = {
    # WAI-NSFW-illustrious-SDXL v16 (~6.46 GB)
    # VAE уже встроен в модель, отдельный VAE не нужен!
    # CivitAI: https://civitai.com/models/827184/wai-illustrious-sdxl
    "checkpoint": {
        "url": "ВСТАВЬТЕ_ССЫЛКУ_НА_ЯНДЕКС_ДИСК",
        "path": os.path.join(CHECKPOINT_PATH, "waiNSFWillustriousSDXL_v160.safetensors"),
    },
}

# ============================================================================


def get_yandex_download_url(public_url: str) -> str:
    """
    Получает прямую ссылку на скачивание из публичной ссылки Яндекс.Диска.
    """
    api_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download"
    response = requests.get(api_url, params={"public_key": public_url})
    
    if response.status_code != 200:
        raise Exception(f"Failed to get download URL: {response.status_code} - {response.text}")
    
    return response.json()["href"]


def download_file(url: str, destination: str, name: str):
    """
    Скачивает файл с прогрессом.
    """
    # Создаём директорию если не существует
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    
    print(f"\n📥 Downloading {name}...")
    print(f"   Destination: {destination}")
    
    # Получаем прямую ссылку на скачивание
    download_url = get_yandex_download_url(url)
    
    # Скачиваем файл
    response = requests.get(download_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    downloaded = 0
    chunk_size = 8192 * 1024  # 8MB chunks
    
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    mb_downloaded = downloaded / (1024 * 1024)
                    mb_total = total_size / (1024 * 1024)
                    print(f"   Progress: {mb_downloaded:.1f}/{mb_total:.1f} MB ({percent:.1f}%)", end='\r')
    
    print(f"\n   ✓ Downloaded {name} successfully!")


def download_models():
    """
    Скачивает все модели из Яндекс.Диска.
    """
    print("=" * 60)
    print("🚀 Starting model download from Yandex.Disk...")
    print("=" * 60)
    
    for name, config in YANDEX_DISK_LINKS.items():
        url = config["url"]
        path = config["path"]
        
        # Проверяем что ссылка заполнена
        if "ВСТАВЬТЕ_ССЫЛКУ" in url:
            print(f"\n❌ ERROR: Please set Yandex.Disk URL for '{name}' in cache_models.py")
            sys.exit(1)
        
        # Проверяем не скачан ли уже файл
        if os.path.exists(path):
            print(f"\n✓ {name} already exists, skipping...")
            continue
        
        try:
            download_file(url, path, name)
        except Exception as e:
            print(f"\n❌ ERROR downloading {name}: {e}")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ All models downloaded successfully!")
    print("=" * 60)


if __name__ == "__main__":
    download_models()
