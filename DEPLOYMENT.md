# 🚀 Инструкция по развертыванию

## Локальное развертывание

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd tztgbot
```

### 2. Создание виртуального окружения
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка окружения
```bash
cp env.example .env
# Отредактируйте .env файл
```

### 5. Инициализация базы данных
```bash
python init_db.py
```

### 6. Запуск бота
```bash
python run_bot.py
```

## Развертывание на сервере

### 1. Подготовка сервера

#### Ubuntu/Debian
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Установка PostgreSQL (опционально)
sudo apt install postgresql postgresql-contrib -y

# Установка Git
sudo apt install git -y
```

#### CentOS/RHEL
```bash
# Обновление системы
sudo yum update -y

# Установка Python и pip
sudo yum install python3 python3-pip -y

# Установка PostgreSQL (опционально)
sudo yum install postgresql-server postgresql-contrib -y

# Установка Git
sudo yum install git -y
```

### 2. Создание пользователя для бота
```bash
# Создание пользователя
sudo useradd -m -s /bin/bash botuser

# Переключение на пользователя
sudo su - botuser
```

### 3. Клонирование и настройка
```bash
# Клонирование репозитория
git clone <repository-url>
cd tztgbot

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка окружения
cp env.example .env
nano .env
```

### 4. Настройка PostgreSQL (опционально)

#### Создание базы данных
```sql
-- Подключение к PostgreSQL
sudo -u postgres psql

-- Создание базы данных и пользователя
CREATE DATABASE ecommerce_bot;
CREATE USER botuser WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_bot TO botuser;
\q
```

#### Обновление .env
```env
DATABASE_URL=postgresql://botuser:secure_password@localhost:5432/ecommerce_bot
```

### 5. Инициализация базы данных
```bash
python init_db.py
```

### 6. Настройка systemd сервиса

#### Создание файла сервиса
```bash
sudo nano /etc/systemd/system/ecommerce-bot.service
```

#### Содержимое файла сервиса
```ini
[Unit]
Description=E-commerce Telegram Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/tztgbot
Environment=PATH=/home/botuser/tztgbot/venv/bin
ExecStart=/home/botuser/tztgbot/venv/bin/python run_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Запуск сервиса
```bash
# Перезагрузка systemd
sudo systemctl daemon-reload

# Включение автозапуска
sudo systemctl enable ecommerce-bot

# Запуск сервиса
sudo systemctl start ecommerce-bot

# Проверка статуса
sudo systemctl status ecommerce-bot
```

### 7. Настройка логирования
```bash
# Создание директории для логов
sudo mkdir -p /var/log/ecommerce-bot
sudo chown botuser:botuser /var/log/ecommerce-bot

# Обновление .env
echo "LOG_FILE=/var/log/ecommerce-bot/bot.log" >> .env
```

## Docker развертывание

### 1. Создание Dockerfile
```dockerfile
FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание пользователя для безопасности
RUN useradd --create-home --shell /bin/bash botuser
RUN chown -R botuser:botuser /app
USER botuser

# Создание директории для логов
RUN mkdir -p /app/logs

# Команда запуска
CMD ["python", "run_bot.py"]
```

### 2. Создание docker-compose.yml
```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: ecommerce-bot
    restart: unless-stopped
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - ADMIN_USER_ID=${ADMIN_USER_ID}
      - DATABASE_URL=postgresql://botuser:password@db:5432/ecommerce_bot
      - DEBUG=False
      - LOG_LEVEL=INFO
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    depends_on:
      - db
    networks:
      - bot-network

  db:
    image: postgres:15
    container_name: ecommerce-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=ecommerce_bot
      - POSTGRES_USER=botuser
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - bot-network

  redis:
    image: redis:7-alpine
    container_name: ecommerce-redis
    restart: unless-stopped
    networks:
      - bot-network

volumes:
  postgres_data:

networks:
  bot-network:
    driver: bridge
```

### 3. Запуск с Docker Compose
```bash
# Создание .env файла
cp env.example .env
# Отредактируйте .env

# Запуск сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f bot

# Остановка сервисов
docker-compose down
```

## Настройка Nginx (опционально)

### 1. Установка Nginx
```bash
sudo apt install nginx -y
```

### 2. Настройка конфигурации
```bash
sudo nano /etc/nginx/sites-available/ecommerce-bot
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Активация конфигурации
```bash
sudo ln -s /etc/nginx/sites-available/ecommerce-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Мониторинг и логирование

### 1. Настройка logrotate
```bash
sudo nano /etc/logrotate.d/ecommerce-bot
```

```
/var/log/ecommerce-bot/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 botuser botuser
    postrotate
        systemctl reload ecommerce-bot
    endscript
}
```

### 2. Мониторинг с помощью systemd
```bash
# Просмотр логов
sudo journalctl -u ecommerce-bot -f

# Статистика сервиса
sudo systemctl status ecommerce-bot

# Перезапуск сервиса
sudo systemctl restart ecommerce-bot
```

### 3. Настройка алертов
```bash
# Создание скрипта мониторинга
sudo nano /usr/local/bin/bot-monitor.sh
```

```bash
#!/bin/bash
if ! systemctl is-active --quiet ecommerce-bot; then
    echo "E-commerce bot is down!" | mail -s "Bot Alert" admin@example.com
    systemctl restart ecommerce-bot
fi
```

```bash
# Добавление в crontab
sudo crontab -e
# Добавить строку:
*/5 * * * * /usr/local/bin/bot-monitor.sh
```

## Резервное копирование

### 1. Скрипт резервного копирования
```bash
nano /home/botuser/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/botuser/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Создание директории для бэкапов
mkdir -p $BACKUP_DIR

# Резервное копирование базы данных
if [ -f "ecommerce_bot.db" ]; then
    cp ecommerce_bot.db $BACKUP_DIR/ecommerce_bot_$DATE.db
fi

# Резервное копирование логов
if [ -d "logs" ]; then
    tar -czf $BACKUP_DIR/logs_$DATE.tar.gz logs/
fi

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

### 2. Автоматическое резервное копирование
```bash
chmod +x /home/botuser/backup.sh

# Добавление в crontab
crontab -e
# Добавить строку:
0 2 * * * /home/botuser/backup.sh
```

## Обновление бота

### 1. Скрипт обновления
```bash
nano /home/botuser/update.sh
```

```bash
#!/bin/bash
cd /home/botuser/tztgbot

# Остановка сервиса
sudo systemctl stop ecommerce-bot

# Создание резервной копии
./backup.sh

# Обновление кода
git pull origin main

# Активация виртуального окружения
source venv/bin/activate

# Обновление зависимостей
pip install -r requirements.txt

# Применение миграций (если есть)
# python manage.py migrate

# Запуск сервиса
sudo systemctl start ecommerce-bot

echo "Update completed"
```

### 2. Запуск обновления
```bash
chmod +x /home/botuser/update.sh
./update.sh
```

## Безопасность

### 1. Настройка файрвола
```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# iptables (CentOS)
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -P INPUT DROP
```

### 2. Настройка SSL (Let's Encrypt)
```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx -y

# Получение сертификата
sudo certbot --nginx -d your-domain.com

# Автоматическое обновление
sudo crontab -e
# Добавить строку:
0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Ограничение доступа к базе данных
```bash
# PostgreSQL
sudo nano /etc/postgresql/*/main/pg_hba.conf
# Изменить на:
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

## Производительность

### 1. Оптимизация базы данных
```sql
-- Создание индексов
CREATE INDEX idx_users_telegram_id ON users(telegram_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
```

### 2. Настройка PostgreSQL
```bash
sudo nano /etc/postgresql/*/main/postgresql.conf
```

```
# Основные настройки
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
```

### 3. Мониторинг производительности
```bash
# Установка htop
sudo apt install htop -y

# Мониторинг ресурсов
htop

# Мониторинг дискового пространства
df -h

# Мониторинг использования памяти
free -h
```

---

**Следуйте этим инструкциям для надежного развертывания вашего E-commerce Telegram бота!**
