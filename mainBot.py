from telegram import Update
from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
import requests
import io


def downloader(bot, url, timeout=None):
    # if you receive a timeout error, pass an increasing timeout until you don't
    buf = bot.request.retrieve(url, timeout=timeout)
    # turning the byte stream into a file_like object without actually writing it to a file
    file_like = io.BytesIO(buf)
    # and returning it
    return buf


def get_text_from_voice(file, context: CallbackContext):
    api_url = 'https://speech-recognition-english.p.rapidapi.com/api/asr'
    api_key = '6fb27ba8ddmsh97f92d7410fa53cp149d50jsnf12fa283fb2e'

    voice_as_bytes = downloader(context.bot, file.file_path)

    files = {'sound': ('voice', voice_as_bytes, 'multipart/form-data')}
    header = {
        "x-rapidapi-host": "speech-recognition-english.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }
    print("request is sent")
    response = requests.post(api_url, files=files, headers=header)
    print("response was received", response)
    return str(response.json())


def voice_handler(update: Update, context: CallbackContext):
    print("input is in the house")
    file = context.bot.getFile(update.message.voice.file_id)
    msg = get_text_from_voice(file, context)
    chat_id = update.message.chat_id
    print("msg to be sent")
#    context.bot.send_voice(chat_id=chat_id, voice=file.file_path)
    context.bot.send_message(chat_id=chat_id, text=msg)


def audio_handler(update: Update, context: CallbackContext):
    print("input is in the house")
    file = context.bot.getFile(update.message.document.file_id)
    msg = get_text_from_voice(file, context)
    chat_id = update.message.chat_id
    print("msg to be sent")
#    context.bot.send_voice(chat_id=chat_id, voice=file.file_path)
    context.bot.send_message(chat_id=chat_id, text=msg)


def printer(update: Update, context: CallbackContext):
    print(update.message)


def main():
    updater = Updater(token='1422402299:AAFZFYZfLmzOTjn6ZZseMiBmKl_P9t85XmI', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    dp.add_handler(MessageHandler(Filters.document.wav, audio_handler))
#    dp.add_handler(MessageHandler(Filters.all, printer))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
