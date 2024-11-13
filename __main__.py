import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.input_stream import AudioPiped
from pyrogram import Client
from pyrogram.types import Message
from youtube_dl import YoutubeDL

# Initialize the Pyrogram Client and PyTgCalls
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'
SESSION_NAME = 'YOUR_SESSION_NAME'

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
bot = Bot(BOT_TOKEN)
pytgcalls = PyTgCalls(app)

# Set up the download options for YouTube audio
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm your group video chat music player bot. Use /play <URL> to play music.")

async def play(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Please provide a YouTube URL after the /play command.")
        return

    url = context.args[0]
    chat_id = update.message.chat.id

    # Download audio from YouTube
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict).replace(".webm", ".mp3")

    # Start streaming audio in group voice chat
    await pytgcalls.join_group_call(chat_id, AudioPiped(audio_file))
    await update.message.reply_text(f"Playing music from {url}.")

async def stop(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await update.message.reply_text("Stopped the music and left the voice chat.")

# Register commands with Updater
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("play", play))
    dp.add_handler(CommandHandler("stop", stop))

    # Start polling and PyTgCalls
    updater.start_polling()
    app.start()
    pytgcalls.start()
    
    # Run the bot until it is stopped
    idle()
    updater.idle()

if __name__ == '__main__':
    main()
