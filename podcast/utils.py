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

    def parse_podcast(self):
        channel = self.root.find('channel')
        # for tag in list(channel.iter())[:20]:
        #     print(tag.tag)
        assert channel,'There is no channel'
        for field in self.podcst_fields:
            self.podcast_dict[field]=self.get_text(channel, field)
        return self.podcast_dict
    
    def parse_episode(self):
        itemlist = self.root.findall('./channel/item')
        for item in itemlist:  #because we have some items
            item_epi_dict={}
            for field in self.episode_field:
                item_epi_dict[field]=self.get_text(item, field)
            self.episode_list.append(item_epi_dict)
        return self.episode_list
    


                
