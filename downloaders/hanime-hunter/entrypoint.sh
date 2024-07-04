#!/usr/bin/env bash
groupmod -o -g ${PGID} hanihunter
usermod -o -u ${PUID} hanihunter
chown -R hanihunter:hanihunter /app
umask ${UMASK}
exec su-exec hanihunter:hanihunter $@