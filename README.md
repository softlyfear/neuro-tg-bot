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
Создайте файл .env в корневой папке по такому шаблону, см. пункт 4 ниже
```
TELEGRAM_API_KEY=<YOUR BOT TOKEN>
OPENAI_API_KEY=<YOUR GPT TOKEN>
PROXY_HTTP=<YOUR HTTP PROXY>
# proxy format http://login:password@ip:port
```

#### Установка на Linux сервере(ubuntu)

##### 1. Обновление сервера
```bash
sudo apt update && sudo apt upgrade -y
```

##### 2. Клонирование репозитория
```bash
git clone https://github.com/softlyfear/neuro-tg-bot
```

##### 3. Установка и активация виртуального окружения
```bash 
cd neuro-tg-bot
apt install python3-venv -y
python3 -m venv .venv
source .venv/bin/activate
```

##### 4. Создание и редактирование файла .env
```bash
echo "TELEGRAM_API_KEY=<YOUR BOT TOKEN>" > .env
echo "OPENAI_API_KEY=<YOUR GPT TOKEN>" >> .env
echo "PROXY_HTTP=<YOUR HTTP PROXY>" >> .env
nano .env
# ctrl+X Y Enter  сохранить изменения
# proxy format http://login:password@ip:port
```

##### 5. Установка зависимостей
```bash 
pip install -r requirements.txt
# Ручная установка
# pip install aiogram
# pip install openai
# pip install dotenv
```

##### 6. Создание tmux сессии и запуск бота
```bash
tmux new -s tg_bot
python3 main.py
# ctrl+B D  выйти из сессии
# tmux attach -t tg_bot  прикрепиться к сессии 
# exit  убить сессию
```