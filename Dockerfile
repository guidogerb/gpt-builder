# 'dev' or 'release' container build
ARG BUILD_TYPE=dev

# Use an official Python base image from the Docker Hub
FROM python:3.12-slim AS guidogerb-base

# Install browsers
RUN apt-get update && apt-get install -y \
    chromium-driver firefox-esr ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install utilities
RUN apt-get update && apt-get install -y \
    curl jq wget git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PIP_NO_CACHE_DIR=yes \
    PYTHONUNBUFFERED=1

# Install the required python packages globally
ENV PATH="$PATH:/root/.local/bin"
COPY guidogerb/config/requirements.txt .

# Set the entrypoint
ENTRYPOINT ["python", "-m", "builder", "--install-plugin-deps"]

# dev build -> include everything
FROM guidogerb-base as guidogerb-dev
RUN pip install --no-cache-dir -r ./guidogerb/config/requirements.txt
WORKDIR /app
ONBUILD COPY guidogerb/ ./builder
ONBUILD RUN mkdir ./output

# release build -> include bare minimum
FROM guidogerb-base as guidogerb-release
RUN sed -i '/Items below this point will not be included in the Docker Image/,$d' ./guidogerb/config/requirements.txt && \
	pip install --no-cache-dir -r ./guidogerb/config/requirements.txt
WORKDIR /app
ONBUILD COPY guidogerb/ ./builder
ONBUILD RUN mkdir ./output

FROM guidogerb-${BUILD_TYPE} AS guidogerb