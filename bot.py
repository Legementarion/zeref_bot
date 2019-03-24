import config
import telebot
import requests
import json

bot = telebot.TeleBot(config.token)


@bot.channel_post_handler(content_types=['text', 'audio', 'document', 'photo', 'video'])
def post_handler(message):
    # sending get request and saving the response as response object
    # response = requests.get(url=config.telegram_url, params=params)

    # extracting data in json format
    response = requests.get('http://api.telegram.org/bot{}/getFile?file_id={}'
                            .format(config.token, message.photo[-1]
                                    .file_id))

    if response.status_code == 200:
        data = json.loads(response.text)
        file_url = config.telegram_url + data['result']['file_path']

        new_data = '''{
            "embeds": [{
                "image": {
                    "url": "''' + file_url + '''"
                }
            }]
        }'''
        headers = {'Content-type': 'application/json'}
        requests.post(config.discord_web_hook, data=new_data, headers=headers)


bot.polling()
