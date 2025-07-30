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

#### Установка на Linux сервере(ubuntu)

##### 1. Обновление сервера и установка зависимостей

```bash
sudo apt update && sudo apt upgrade -y
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

##### 2. Установка бота и зависимостей

##### 3. Создание и редактирование файла .env

```bash
cd app/configs/
echo "TELEGRAM_API_KEY=<YOUR BOT TOKEN>" > .env
echo "OPENAI_API_KEY=<YOUR GPT TOKEN>" >> .env
echo "PROXY_HTTP=<YOUR HTTP PROXY>" >> .env
nano .env
# ctrl+X Y Enter  сохранить изменения
# proxy format http://login:password@ip:port
```

##### 4. Создание tmux сессии

```bash
cd ../..
tmux new -s tg_bot
# ctrl+B D  выйти из сессии
# tmux attach -t tg_bot  прикрепиться к сессии 
# exit  убить сессию
```

##### 5. Запуск бота

```bash
uv run python3 main.py
```