import traceback
import telegram
import requests
import time


def worker(iteration_delay, channels_groups, telegram_token, vk_service_code):
    while True:
        try:
            worker_iteration(channels_groups, telegram_token, vk_service_code)
        except:
            traceback.print_exc()
        time.sleep(iteration_delay)


def worker_iteration(channels_groups, telegram_token, vk_service_code):
    bot = telegram.Bot(telegram_token)

    for channel, groups in channels_groups.items():
        for group in groups:
            posts = fetch_group_posts(group, vk_service_code)

            for post in posts:
                post_url = 'https://vk.com/wall{}_{}'.format(group, post['id'])
                text = '{}\n\n{}'.format(post_url, post['text'])
                has_photo = 'attachments' in post and 'photo_1280' in post['attachments'][0]

                bot.send_message(channel, text)
                if has_photo:
                    photo_url = post['attachments'][0]['photo_1280']
                    bot.send_photo(channel, photo_url)


def fetch_group_posts(group, vk_service_code):
    r = requests.get('https://api.vk.com/method/wall.get?domain={}&count=10&secure={}&v=5.63'.format(group, vk_service_code))
    return r.json()['response']['items']