from io import BytesIO

from PIL import Image
import config
import telebot
import json
import requests
import urllib.request
import tempfile

from dhooks import Webhook, File

hook = Webhook(config.discord_web_hook)

bot = telebot.TeleBot(config.token)


@bot.channel_post_handler(content_types=['text', 'audio', 'document', 'photo', 'video'])
def post_handler(message):
    response = requests.get('http://api.telegram.org/bot{}/getFile?file_id={}'
                            .format(config.token, message.photo[-1]
                                    .file_id))

    if response.status_code == 200:
        data = json.loads(response.text)
        file_url = config.telegram_url + data['result']['file_path']
        fd = urllib.request.urlopen(file_url)
        img = Image.open(BytesIO(fd.read()))

        tmpfile = tempfile.TemporaryFile()
        img.save(tmpfile, "PNG")
        tmpfile.seek(0)
        file = File(tmpfile, name='bluepost.png')  # optional name for discord

        hook.send('Look at this:', file=file)


bot.polling()
