import xml.etree.ElementTree as ET
from .models import Podcast, Episode

class XMLParser:
    episode_field=[ 'title', 'description', 'image', 'author', 'pubDate','episodeType', 'summary', 'guid', 'explicit', 'keywords', 'duration','contentEncoded', 'podcast']
    podcst_fields=['title', 'description', 'generator', 'copyright', 'link', 'pubDate', 'itunes:summary','itunes:type', 'itunes:explicity', 'itunes:owner','itunes:author','itunes:category','keywords','guid','managingEditor']
    def __init__(self, xml_file):
        self.tree = ET.parse(xml_file)
        self.root = self.tree.getroot()
        self.namespaces = {
            'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
        }

    def get_text(self, node, path, default=""):
        element = node.find(path, namespaces=self.namespaces)
        return element.text if element is not None else default

    def parse(self):
        channel = self.root.find('channel')
        if channel:
            podcast = Podcast.objects.create(
                title=self.get_text(channel, 'title'),
                generator=self.get_text(channel, 'generator'),
                description=self.get_text(channel, 'description'),
                copyright=self.get_text(channel, 'copyright'),
                language=self.get_text(channel, 'language')
            )

            for item in channel.findall('item'):
                Episode.objects.create(
                    podcast=podcast,
                    title=self.get_text(item, 'title'),
                    description=self.get_text(item, 'description'),
                    pubDate=self.get_text(item, 'pubDate')
                )
