import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pymongo import MongoClient

# Config
TOKEN_BOT = os.environ.get("TOKEN_BOT")  # Ambil dari Railway Environment
MONGODB_URI = os.environ.get("MONGODB_URI")  # Ambil dari Railway Environment

# Setup MongoDB
client = MongoClient(MONGODB_URI)
db = client["coin_db"]
users = db["users"]

# Command /start
def start(update: Update, context: CallbackContext) -> None:
    user_name = update.effective_user.first_name
    update.message.reply_text(f"Hai {user_name}! Ketik /klaim untuk dapat koin!")

# Command /klaim
def klaim(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user = users.find_one({"user_id": user_id})
    
    if user:
        new_coin = user.get("coin", 0) + 10
        users.update_one({"user_id": user_id}, {"$set": {"coin": new_coin}})
    else:
        users.insert_one({"user_id": user_id, "coin": 10, "name": update.effective_user.first_name})
        new_coin = 10
    
    update.message.reply_text(f"🎉 +10 Koin! Total: {new_coin}")

# Command /cek
def cek(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    user = users.find_one({"user_id": user_id})
    update.message.reply_text(f"🪙 Total koin: {user['coin'] if user else 0}")

# Jalankan Bot
if __name__ == "__main__":
    updater = Updater(TOKEN_BOT)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("klaim", klaim))
    dispatcher.add_handler(CommandHandler("cek", cek))
    updater.start_polling()
    updater.idle()
