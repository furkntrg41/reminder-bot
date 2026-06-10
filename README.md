# Reminder Bot

Telegram hatırlatıcı bot — APScheduler ile belirli tarih ve saatlerde mesaj gönderir.

## Komutlar

| Komut | Açıklama |
|-------|---------|
| `/ekle GG.AA.YYYY SS:DD mesaj` | Tek seferlik hatırlatma ekle |
| `/listele` | Aktif hatırlatmaları listele |
| `/sil <id>` | Hatırlatma sil |

## Teknolojiler

- **python-telegram-bot** — Telegram Bot API
- **APScheduler** — zamanlama motoru  
- **JSON** — kalıcı depolama

## Kurulum

```bash
pip install -r requirements.txt
BOT_TOKEN=your_token python telebot.py
```

## Deployment

Railway üzerinde `worker` olarak çalışır. `DATA_DIR=/data` environment variable ile kalıcı depolama sağlanır.
