from diary_bot.config.settings import settings
import requests
from datetime import datetime


class LskyService:
    def __init__(self):
        self.uri = settings.LSKY_URI
        self.email = settings.LSKY_EMAIL
        self.password = settings.LSKY_PASSWORD

    def get_token(self):
        get_token_uri = self.uri + '/tokens'
        data = requests.post(get_token_uri, json={
            'email': self.email,
            "password": self.password
        },verify=False).json()
        if data['status']:
            return data["data"]['token']

    def get_images(self):
        get_images_uri = self.uri + '/images'
        data = requests.get(get_images_uri, headers={'Authorization': 'Bearer ' + self.get_token()}, params={
            "order": "newest",

        },verify=False).json()
        images = []
        if data['status']:
            for image in data['data']['data']:
                date_obj = datetime.strptime(image['date'], "%Y-%m-%d %H:%M:%S")
                if date_obj.date() == datetime.today().date():
                    images.append(image)
        return images
