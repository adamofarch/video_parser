FROM archlinux:latest

ENV PYTHONUNBUFFERED 1

# Enable BuildKit-specific features
ARG BUILDKIT_INLINE_CACHE=1

# Combine RUN commands and use mount cache for apt and pip
RUN pacman -Sy --noconfirm && \
  pacman -S --noconfirm \
  base-devel \
  cmake \
  pkg-config \
  ffmpeg \
  tesseract \
  leptonica \
  curl \
  glib2 \
  gpac \
  postgresql-libs \
  postgresql \
  git \
  wget \
  python \
  python-pip 

RUN useradd -m -s /bin/bash builder && \
  echo "builder ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Switch to the non-root user
USER builder
WORKDIR /home/builder

RUN sudo pacman -S --noconfirm --needed git base-devel && \
  git clone https://aur.archlinux.org/yay.git /tmp/yay && \
  cd /tmp/yay && \
  makepkg -si --noconfirm && \
  cd / && \
  sudo rm -rf /tmp/yay

RUN yay -S --noconfirm ccextractor

USER root

WORKDIR /app

# Use mount cache for pip
COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
  pip install --break-system-packages -r requirements.txt

COPY . .

RUN mkdir -p /app/Temp
RUN chown -R builder:builder /app/Temp
RUN chmod -R 777 /app/Temp

RUN cp .env.example .env

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
