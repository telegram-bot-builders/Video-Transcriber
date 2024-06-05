from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from whisperHandler import Whisperer
import fileConverters, keyHolder
import os
import logging
from transcribe import extract_audio

# Setting up the whisperer
whisperer = Whisperer(
    keyHolder.openaiApiKey
)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Send me a video message and I will extract the audio for you.')

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='File received')
    try:
        file = None
        if update.message.audio:
            file = update.message.audio
        elif update.message.video:
            file = update.message.video
        elif update.message.document:
            file = update.message.document
        audio_file = await context.bot.get_file(file.file_id)
        filename = f'{file.file_name.split(".")[0]}'
        print(filename)
        print(filename)
        print(filename)
        print(filename)
        print(filename)
        fileExtension = os.path.splitext(filename)[1][1:]
        await audio_file.download_to_drive(f'{filename}{fileExtension}')
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Converting')
        await fileConverters.auto_to_mp3(filename, fileExtension)
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Transcribing')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Text: " + await whisperer.whisp(filename + '.mp3'))
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Free to use != free of costs, consider donating! https://www.buymeacoffee.com/FosanzDev')
        # send the audio file to the user
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(f'{filename}.mp3', 'rb'))
    except Exception as e:
        logger.error(f'Error processing video: {e}')
        await update.message.reply_text('Sorry, I could not process your video.')

def main():
    application = ApplicationBuilder().token(keyHolder.telegramApiKey).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Document.AUDIO | filters.AUDIO | filters.VIDEO | filters.Document.VIDEO & (~filters.COMMAND), handle_video, block=False))

    application.run_polling()

if __name__ == '__main__':
    main()