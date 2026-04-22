# Base image with CUDA 12.9 for compute capability 12.0 support
FROM runpod/base:1.0.3-cuda1290-ubuntu2204

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
