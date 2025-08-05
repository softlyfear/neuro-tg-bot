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
WORKDIR /neuro-tg-bot

# Копируем репозиторий
COPY . .

# Устанавливаем зависимости
RUN uv sync

# Запускаем бота
CMD ["uv", "run", "python3", "main.py"]