# Base image with CUDA 12.1 for better compatibility
FROM runpod/base:0.6.2-cuda12.1.0

ENV HF_HUB_ENABLE_HF_TRANSFER=0
ENV TRANSFORMERS_CACHE=/models/cache
ENV HF_HOME=/models/cache

# Install Python dependencies
COPY builder/requirements.txt /requirements.txt
RUN python3.11 -m pip install --upgrade pip && \
    python3.11 -m pip install --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# Download models from Yandex.Disk
COPY builder/cache_models.py /cache_models.py
RUN python3.11 /cache_models.py && \
    rm /cache_models.py

# Add src files
ADD src .

CMD python3.11 -u /rp_handler.py
