import logging
import json
import os
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger

# scheduler ve bot referansı - tüm fonksiyonlar bunları kullanacak
scheduler = AsyncIOScheduler(timezone="Europe/Istanbul")
bot_instance = None

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba Furkan! Reminder Bot devrede.")

async def ekle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    parcalar = context.args[0].split(".")
    gun = int(parcalar[0])
    ay = int(parcalar[1])
    yil = int(parcalar[2]) if len(parcalar) == 3 else datetime.now().year

    parcalar2 = context.args[1:]
    if ":" in parcalar2[0]:
        saat_parcalari = parcalar2[0].split(":")
        saat = int(saat_parcalari[0])
        dakika = int(saat_parcalari[1])
        not_ = " ".join(parcalar2[1:])
    else:
        saat, dakika = 9, 0
        not_ = " ".join(parcalar2)

    event = datetime(yil, ay, gun, saat, dakika)

    dosya = os.path.join(os.path.dirname(__file__), "reminders.json")

    if os.path.exists(dosya):
        with open(dosya, "r", encoding="utf-8") as f:
            liste = json.load(f)
    else:
        liste = []

    # Yeni hatırlatıcıyı ekle
    liste.append({
        "chat_id": update.effective_chat.id,
        "tarih": event.isoformat(),
        "not": not_
    })

    # Geri yaz
    with open(dosya, "w", encoding="utf-8") as f:
        json.dump(liste, f, ensure_ascii=False, indent=2)

    # Scheduler'a job ekle
    chat_id = update.effective_chat.id
    now = datetime.now()

    bir_gun_once  = event - timedelta(days=1)
    bir_saat_once = event - timedelta(hours=1)

    # Her birini sadece henüz geçmemişse ekle
    if bir_gun_once > now:
        scheduler.add_job(bildirim_gonder, DateTrigger(run_date=bir_gun_once),
                          args=[chat_id, f"Yarin: {not_}\n{event.strftime('%d.%m.%Y %H:%M')}"])

    if bir_saat_once > now:
        scheduler.add_job(bildirim_gonder, DateTrigger(run_date=bir_saat_once),
                          args=[chat_id, f"1 saat sonra: {not_}\n{event.strftime('%d.%m.%Y %H:%M')}"])

    if event > now:
        scheduler.add_job(bildirim_gonder, DateTrigger(run_date=event),
                          args=[chat_id, f"Simdi: {not_}"])

    await update.message.reply_text(
        f"Kaydedildi!\n"
        f"Ne zaman: {event.strftime('%d.%m.%Y %H:%M')}\n"
        f"Not: {not_}"
    )


async def liste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dosya = os.path.join(os.path.dirname(__file__), "reminders.json")

    if not os.path.exists(dosya):
        await update.message.reply_text("Hic hatirlatici yok.")
        return

    with open(dosya, "r", encoding="utf-8") as f:
        kayitlar = json.load(f)
    if not kayitlar:
        await update.message.reply_text("Hic hatirlatici yok.")
        return

    mesaj = "Hatirlaticilar:\n"
    now = datetime.now()
    gelecek = sorted(
        [r for r in kayitlar if datetime.fromisoformat(r["tarih"]) > now],
        key=lambda r: r["tarih"]   # en yakından en uzağa
    )

    if not gelecek:
        await update.message.reply_text("Gelecek hatirlatici yok.")
        return

    for i, r in enumerate(gelecek):
        dt = datetime.fromisoformat(r["tarih"])
        mesaj += f"{i+1}. {dt.strftime('%d.%m.%Y %H:%M')} - {r['not']}\n"

    await update.message.reply_text(mesaj)

# Bot ilk başladığında çalışır
async def baslangic(app):
    global bot_instance
    bot_instance = app
    scheduler.start()
    scheduler.add_job(
        sabah_ozeti,
        CronTrigger(hour=9, minute=0, timezone="Europe/Istanbul"),
        id="sabah_ozeti",
        replace_existing=True
    )
    

# Bildirim gönderici - scheduler bu fonksiyonu çağırır
async def bildirim_gonder(chat_id, metin):
    await bot_instance.bot.send_message(chat_id=chat_id, text=metin)

# Her sabah 09:00'da çalışır - o gün ne var varsa yazar
async def sabah_ozeti():
    dosya = os.path.join(os.path.dirname(__file__), "reminders.json")
    if not os.path.exists(dosya):
        return

    with open(dosya, "r", encoding="utf-8") as f:
        kayitlar = json.load(f)

    bugun = datetime.now().strftime("%Y-%m-%d")

    # Bugüne ait kayıtları bul (tarih kısmı eşleşenler)
    bugunun = [r for r in kayitlar if r["tarih"].startswith(bugun)]

    if not bugunun:
        return  # bugün hiçbir şey yok, sessiz kal

    # Her kullanıcıya ayrı mesaj gönder
    chat_ids = {r["chat_id"] for r in bugunun}
    for cid in chat_ids:
        benim = [r for r in bugunun if r["chat_id"] == cid]
        mesaj = "☀️ Bugun ne var:\n"
        for r in benim:
            dt = datetime.fromisoformat(r["tarih"])
            mesaj += f"  • {dt.strftime('%H:%M')} - {r['not']}\n"
        await bildirim_gonder(cid, mesaj)



async def test_ozet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sabah ozetini simdi gonder - test icin"""
    await sabah_ozeti()
    await update.message.reply_text("Sabah ozeti gonderildi (test).")


async def bugun(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dosya = os.path.join(os.path.dirname(__file__), "reminders.json")
    if not os.path.exists(dosya):
        await update.message.reply_text("Bugun hicbir sey yok.")
        return

    with open(dosya, "r", encoding="utf-8") as f:
        kayitlar = json.load(f)

    bugun_str = datetime.now().strftime("%Y-%m-%d")
    bugunun = sorted(
        [r for r in kayitlar if r["tarih"].startswith(bugun_str)],
        key=lambda r: r["tarih"]
    )

    if not bugunun:
        await update.message.reply_text("Bugun hicbir sey yok.")
        return

    mesaj = "Bugun:\n"
    for r in bugunun:
        dt = datetime.fromisoformat(r["tarih"])
        mesaj += f"  • {dt.strftime('%H:%M')} - {r['not']}\n"

    await update.message.reply_text(mesaj)


if __name__ == '__main__':
    # Railway'de TOKEN environment variable olarak verilecek
    # Lokalde token.txt'den okur
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        TOKEN = open(os.path.join(os.path.dirname(__file__), "token.txt")).read().strip()

    application = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(baslangic)   # bot hazır olunca baslangic() çalışır
        .build()
    )

    application.add_handler(CommandHandler('start',    start))
    application.add_handler(CommandHandler('ekle',     ekle))
    application.add_handler(CommandHandler('liste',    liste))
    application.add_handler(CommandHandler('bugun',    bugun))
    application.add_handler(CommandHandler('test',     test_ozet))

    print("Bot çalışıyor...")
    application.run_polling()
