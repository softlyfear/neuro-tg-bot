# 🤖 Neuro-TG-Bot - Telegram-помощник c GPT

#### Телеграм бот со встроенной языковой моделью gpt 4

#### Доступный функционал:

1. Чат с GPT - Ведите интеллектуальные диалоги с GPT
2. Генератор случайных фактов - Получайте интересные и неожиданные факты
3. Квиз - Проверяйте свои знания в различных категориях
4. Переводчик - Быстро переводите текст на выбранные языки
5. Диалог с известной личностью - Ведите диалог с предложенной личностью
6. Рекомендации по фильмам и книгам - Рекомендации по жанрам

#### Файл .env не отслеживается в .gitignore

Создайте файл .env в папке app/configs по такому шаблону, см. пункт 3 ниже

```
TELEGRAM_API_KEY=<YOUR BOT TOKEN>
OPENAI_API_KEY=<YOUR GPT TOKEN>
PROXY_HTTP=<YOUR HTTP PROXY>
# proxy format http://login:password@ip:port
```

#### Установка CLI версии

##### 1.1 Обновление сервера и установка пакетов

```bash
sudo apt update && sudo apt upgrade -y
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

##### 1.2 Установка бота и зависимостей

```bash
git clone https://github.com/softlyfear/neuro-tg-bot
cd neuro-tg-bot/
uv sync
```

##### 1.3 Создание и редактирование файла .env

```bash
cd app/configs/
echo "TELEGRAM_API_KEY=<YOUR BOT TOKEN>" > .env
echo "OPENAI_API_KEY=<YOUR GPT TOKEN>" >> .env
echo "PROXY_HTTP=<YOUR HTTP PROXY>" >> .env
nano .env
# ctrl+X Y Enter  сохранить изменения
# proxy format http://login:password@ip:port
```

##### 1.4 Создание tmux сессии

```bash
cd ../..
tmux new -s tg_bot
# ctrl+B D  выйти из сессии
# tmux attach -t tg_bot  прикрепиться к сессии 
# exit  убить сессию
```

##### 1.5 Запуск бота

```bash
uv run python3 main.py
```

#### Установка Docker версии

##### 2. 1 Устанавливаем докер

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# Install the Docker packages
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

##### 2.2 Клонируем репозиторий

```bash
git clone https://github.com/softlyfear/neuro-tg-bot
cd neuro-tg-bot/
```

##### 2.3 Создаем образ

```bash
sudo docker build -t neuro-tg-bot .
# neuro-tg-bot можете заменить на свое название
```

##### 2.4 Запускаем в фоновом режиме с передачей .ENV токенов

```bash
# Значения внутри <> и "" замените на свои токены
sudo docker run -d \
    -e TELEGRAM_API_KEY=<YOUR BOT TOKEN> \
    -e OPENAI_API_KEY=<YOUR GPT TOKEN> \
    -e PROXY_HTTP="YOUR HTTP PROXY" \
    neuro-tg-bot
```