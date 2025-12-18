# main.py
from telethon import TelegramClient
import asyncio
import random
from datetime import datetime
from fastapi import FastAPI
import uvicorn
import os

# ====== KONFIGURASI ======

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = "/tmp/session_tele_user"  # Render hanya bisa write ke /tmp

GROUP_IDS = [
    -1002658447462,
    -1002255700000,
    -1001428379167,
    -1001706294440,
    -1002072882843,
    -1001352580530,
    -1001662248944,
    -1002038560278,
    -1001662248944,
    -1001764400714,
    -1001684579817
]

MESSAGES = [
    "🔥 GRATISAN LAGI DIBUKA 🔥\nYang nanya free? 👉 Sudah tersedia di BIO\nTanpa deposit\nLangsung klaim\nGas cek bio sekarang 💥",
    "🎁 INFO FREEBET HARI INI 🎁\nGratis tanpa deposit, langsung klaim di BIO!\nKesempatan terbatas ⚡",
    "⚡ PROMO GRATIS ⚡\nSudah ada di BIO, jangan sampai kelewatan\nLangsung klaim sekarang!"
]

LOG_FILE = "/tmp/log_telegram.txt"

# ====== Fungsi utama ======
async def send_messages():
    async with TelegramClient(session_name, api_id, api_hash) as client:
        for group_id in GROUP_IDS:
            try:
                message = random.choice(MESSAGES)
                await client.send_message(group_id, message)
                log_text = f"{datetime.now()} - Berhasil kirim ke {group_id}"
                print(log_text)
                with open(LOG_FILE, "a") as f:
                    f.write(log_text + "\n")

                # Delay acak 5-15 detik untuk mengurangi risiko spam
                await asyncio.sleep(random.randint(5, 15))
            except Exception as e:
                log_text = f"{datetime.now()} - Gagal kirim ke {group_id}: {e}"
                print(log_text)
                with open(LOG_FILE, "a") as f:
                    f.write(log_text + "\n")

# ====== FastAPI setup untuk Render ======
app = FastAPI()

@app.get("/send")
async def trigger_send():
    await send_messages()
    return {"status": "success", "message": "Pesan terkirim!"}

# ====== Entry point untuk lokal testing ======
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), log_level="info")
