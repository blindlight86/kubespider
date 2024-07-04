# syntax=docker/dockerfile:1

FROM python:3.10-alpine

ENV HOME="/app" \
    PUID=1000 \
    PGID=1000 \
    UMASK=022 \
    TZ=Asia/Shanghai

WORKDIR /app

COPY requirements.txt ./
COPY app app

RUN set -ex \
    && apk add --no-cache \
        bash \
        su-exec \
        tzdata \
        shadow \
        ffmpeg \
        curl \
        jq \
        tar \
    && mkdir -p /app/downloads \
    && mkdir -p /app/config \
    && python3 -m pip install --upgrade pip \
    && pip install -r requirements.txt \
    && addgroup -S hanihunter -g 911 \
    && adduser -S hanihunter -G hanihunter -h /app -u 911 -s /bin/bash hanihunter \
    && rm -rf \
        /app/.cache \
        /tmp/*

RUN curl -s https://api.github.com/repos/acgtools/hanime-hunter/releases/latest | \
    jq -r '.assets[] | select(.name | contains("Linux_x86_64.tar.gz")) | .browser_download_url' | \
    xargs curl -L -o hani.tar.gz && \
    tar -xzf hani.tar.gz && \
    mv hani /usr/local/bin/ && \
    chmod +x /usr/local/bin/hani && \
    rm hani.tar.gz

COPY --chmod=755 entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "bash", "/entrypoint.sh"]

CMD ["python3", "/app/app/app.py"]

EXPOSE 3091