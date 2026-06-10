<div align="center">

# Reminder Bot

**Telegram üzerinden hatırlatma gönderen zamanlama botu**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Railway](https://img.shields.io/badge/Deployed-Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)](https://railway.app)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

</div>

---

## Özellikler

- Belirli tarih ve saatte tek seferlik hatırlatma ekleme
- Aktif hatırlatmaları listeleme ve silme
- JSON dosyasında kalıcı depolama (yeniden başlatmaya dayanıklı)
- Railway üzerinde `worker` olarak çalışır

---

## Komutlar

| Komut | Format | Açıklama |
|-------|--------|---------|
| `/ekle` | `/ekle GG.AA.YYYY SS:DD mesajınız` | Yeni hatırlatma ekle |
| `/listele` | `/listele` | Aktif hatırlatmaları listele |
| `/sil` | `/sil <id>` | ID'ye göre hatırlatma sil |
| `/start` | `/start` | Bot bilgisi |

**Örnek:**
```
/ekle 25.12.2026 09:00 Yılbaşı alışverişini unutma!
```

---

## Kurulum

### Yerel geliştirme

```bash
# Repo'yu klonla
git clone https://github.com/furkntrg41/reminder-bot.git
cd reminder-bot

# Bağımlılıkları yükle
pip install -r requirements.txt

# Bot token'ı ayarla
export BOT_TOKEN=your_telegram_bot_token

# Botu başlat
python telebot.py
```

### Telegram Bot Token

1. Telegram'da [@BotFather](https://t.me/BotFather) ile yeni bir bot oluşturun
2. Aldığınız token'ı `BOT_TOKEN` environment variable olarak ayarlayın

---

## Deployment (Railway)

1. Repo'yu Railway'e bağlayın
2. Environment variable ekleyin: `BOT_TOKEN=your_token`
3. Kalıcı depolama için: `DATA_DIR=/data`
4. Service type: **Worker** (`Procfile` ile otomatik yapılandırılır)

---

## Proje Yapısı

```
.
├── telebot.py          # Ana bot kodu
├── requirements.txt    # Bağımlılıklar
├── Procfile            # Railway worker tanımı
└── reminders.json      # Kalıcı veri deposu
```

---

## Bağımlılıklar

| Paket | Kullanım |
|-------|---------|
| python-telegram-bot | Telegram Bot API |
| APScheduler | Zamanlama motoru |

---

## Lisans

[MIT](LICENSE) © 2026 furkntrg41
