FROM ubuntu:latest

LABEL authors="Softly"

# Установка зависимостей
RUN apt update && apt upgrade -y && \
    apt install -y curl nano tmux git && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Установка uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Добавляем uv в PATH
ENV PATH="/root/.local/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Клонируем репозиторий
RUN git clone https://github.com/softlyfear/neuro-tg-bot .

# Устанавливаем зависимости
RUN uv sync

# Создаем пустой .env файл
RUN touch /app/app/configs/.env

# Скрипт для интерактивного ввода переменных
RUN echo '#!/bin/bash\n\
if [ ! -s "/app/app/configs/.env" ]; then\n\
    echo "Настройка .env файла..."\n\
    read -p "Введите TELEGRAM_API_KEY: " telegram_key\n\
    read -p "Введите OPENAI_API_KEY: " openai_key\n\
    read -p "Введите PROXY_HTTP (или нажмите Enter для пропуска): " proxy_http\n\
    echo "TELEGRAM_API_KEY=$telegram_key" > /app/app/configs/.env\n\
    echo "OPENAI_API_KEY=$openai_key" >> /app/app/configs/.env\n\
    if [ ! -z "$proxy_http" ]; then\n\
        echo "PROXY_HTTP=$proxy_http" >> /app/app/configs/.env\n\
    fi\n\
    echo ".env файл создан!"\n\
fi\n\
exec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uv", "run", "python3", "main.py"]