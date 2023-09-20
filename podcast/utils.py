import xml.etree.ElementTree as ET
from .models import Podcast, Episode

class XMLParser:
    episode_field=[ 'title', 'description', 'itunes:image', 'author', 'pubDate','itunes:episodeType', 'itunes:summary', 'guid', 'itunes:explicit', 'itunes:keywords', 'itunes:duration','content:encoded', 'podcast']
    podcst_fields=['title', 'description', 'generator', 'copyright', 'link', 'pubDate', 'itunes:summary','itunes:type', 'itunes:explicit','itunes:author','itunes:category','itunes:keywords','managingEditor']
    pod_owner_fields=['itunes:name','itunes:email']
    pod_image_fields=['url','link','title']
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = ET.parse(xml_file,)
        self.root = self.tree.getroot()

    def extract_namespaces(self):
        namespaces = {}
        for event, elem in ET.iterparse(self.xml_file, events=('start', 'end', 'start-ns', 'end-ns')):
            if event == 'start-ns':
                prefix, ns = elem
                namespaces[prefix] = ns
        return namespaces


    def get_text(self, node, path,attrib_key='text', default=""):
        element = node.find(path, namespaces=self.extract_namespaces())
        if element is not None:
            return element.text or element.attrib.get(attrib_key)
        else:
            return default
        
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
    


                
