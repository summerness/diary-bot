from llm.llm import QwenVLService
from blog.blog import HaloService
from lsky.lsky import LskyService

if __name__ == '__main__':
    lsky = LskyService()
    halo = HaloService()
    qwenvl = QwenVLService()
    images = lsky.get_images()
    texts, title = qwenvl.multimodal_conversation_call(images)
    halo.publish_post(images, texts, title)
