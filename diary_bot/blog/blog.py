import json
from datetime import datetime

from diary_bot.config.settings import settings
import requests
from uuid import uuid4
import markdown
from pypinyin import pinyin, Style
from itertools import zip_longest


class HaloService:
    def __init__(self):
        self.api_client = requests.Session()
        self.api_client.headers.update({
            'authorization': f'Bearer {settings.HALO_TOKEN}'
        })
        self.base_url = settings.HALO_URI

    def slugify(self, title):
        slugs = pinyin(title, style=Style.NORMAL)
        texts = []
        for slug in slugs:
            texts.append(slug[0])
        return "-".join(texts)

    def get_post(self, name: str):
        try:
            post = self.api_client.get(f'{self.base_url}/apis/content.halo.run/v1alpha1/posts/{name}').json()
            snapshot = self.api_client.get(
                f'{self.base_url}/apis/content.halo.run/v1alpha1/posts/{name}/draft?patched=true').json()

            content = {
                'content': snapshot.get('metadata', {}).get('annotations', {}).get('content.halo.run/patched-content'),
                'raw': snapshot.get('metadata', {}).get('annotations', {}).get('content.halo.run/patched-raw'),
                'rawType': snapshot.get('spec', {}).get('rawType')
            }
            return {'post': post, 'content': content}
        except Exception as e:
            print(f'Error retrieving post: {e}')
            return None

    def publish_post(self, images, texts, title):
        if len(images) == 0:
            return
        post_uri = f'{self.base_url}/apis/api.console.halo.run/v1alpha1/posts'
        image_links = []
        for index, image in enumerate(images):
            image_links.append(image.get('links').get('markdown_with_link'))

        contents = [item for pair in zip_longest(image_links, texts) for item in pair if item is not None]

        this_date = datetime.now().strftime('%Y-%m-%d')
        raw = "\n\n".join(contents)
        params = {"post": {"spec": {"title": title, "slug": self.slugify(title), "template": "",
                                    "cover": images[0].get('links').get('url'),
                                    "deleted": False, "publish": True, "pinned": False, "allowComment": True,
                                    "visible": "PUBLIC", "priority": 0, "excerpt": {"autoGenerate": True, "raw": ""},
                                    "categories": ["category-fIwwl"], "tags": [], "htmlMetas": []},
                           "apiVersion": "content.halo.run/v1alpha1",
                           "kind": "Post", "metadata": {"name": str(uuid4()),
                                                        "annotations": {
                                                            "content.halo.run/preferred-editor": "vditor-mde"}}},
                  "content": {"raw": raw, "content": markdown.markdown(raw), "rawType": "markdown"}}
        print(self.api_client.post(post_uri, json=params,verify=False).content)

    def get_categories(self):
        response = self.api_client.get(f'{self.base_url}/apis/content.halo.run/v1alpha1/categories')
        return response.json().get('items', [])

    def get_tags(self):
        response = self.api_client.get(f'{self.base_url}/apis/content.halo.run/v1alpha1/tags')
        return response.json().get('items', [])

    def create_category(self, display_name: str):
        category = {
            'spec': {
                'displayName': display_name,
                'slug': self.slugify(display_name),
                'priority': 0
            },
            'apiVersion': 'content.halo.run/v1alpha1',
            'kind': 'Category',
            'metadata': {'generateName': 'category-'}
        }
        response = self.api_client.post(f'{self.base_url}/apis/content.halo.run/v1alpha1/categories', json=category)
        return response.json()

    def create_tag(self, display_name: str):
        tag = {
            'spec': {
                'displayName': display_name,
                'slug': self.slugify(display_name),
                'color': '#ffffff'
            },
            'apiVersion': 'content.halo.run/v1alpha1',
            'kind': 'Tag',
            'metadata': {'generateName': 'tag-'}
        }
        response = self.api_client.post(f'{self.base_url}/apis/content.halo.run/v1alpha1/tags', json=tag)
        return response.json()
