FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

# Enable BuildKit-specific features
ARG BUILDKIT_INLINE_CACHE=1

# Combine RUN commands and use mount cache for apt and pip
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update && apt-get install -y \
  build-essential \
  cmake \
  pkg-config \
  # CCExtractor dependencies
  libglfw3-dev \
  libglfw3 \
  tesseract-ocr \
  # tesseract-dev \
  libleptonica-dev \
  libcurl4-gnutls-dev \
  libglib2.0-dev \
  # PostgreSQL client
  libpq-dev \
  postgresql-client \
  # Utilities
  git \
  wget \
  && rm -rf /var/lib/apt/lists/* \
  && wget https://github.com/CCExtractor/ccextractor/releases/download/v0.94/ccextractor_minimal.tar.gz \
  && apt-get install -y tar \
  && tar -xvf ccextractor_minimal.tar.gz \
  && mv ccextractor /usr/local/bin/ \
  && rm ccextractor_minimal.tar.gz \
  && apt-get remove -y wget \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Use mount cache for pip
COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
  pip install -r requirements.txt

COPY . .

RUN cp .env.example .env

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
