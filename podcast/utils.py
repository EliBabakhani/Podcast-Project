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
        self.episode_list=[]
        self.podcast_dict={}
        self.owner_dict={}
        self.image_dict={}
        self.podcast_object=None


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
    
    def parse_owner_podcast(self):
        channel = self.root.find('./channel/itunes:owner', namespaces=self.extract_namespaces())
        for pif in self.pod_owner_fields:
            self.owner_dict[pif]=self.get_text(channel, pif)
        return self.image_dict

    def parse_image_podcast(self):
        channel = self.root.find('./channel/image', namespaces=self.extract_namespaces())
        for pof in self.pod_image_fields:
            self.owner_dict[pof]=self.get_text(channel, pof)
        return self.owner_dict

    
    def parse_episode(self):
        itemlist = self.root.findall('./channel/item')
        for item in itemlist:  #because we have some items
            item_epi_dict={}
            for field in self.episode_field:
                if field=='itunes:image':
                    item_epi_dict[field]=self.get_text(item, field, attrib_key='href')
                    continue
                item_epi_dict[field]=self.get_text(item, field)

            self.episode_list.append(item_epi_dict)
        return self.episode_list
    
    def save_podcast(self):
        assert not self.check_repeat_podacst,'The Podcast already available'
        new_podcast=dict(map(lambda item:(item[0].replace(':','_'),item[1]),self.parse_podcast().items()))
        podcast=Podcast.objects.create(**new_podcast)
        image=Image.objects.create(**self.image_dict)
        podcast.image=image
        podcast_owner=dict(map(lambda item:(item[0].replace(':','_'),item[1]),self.parse_owner_podcast().items()))
        owner=Owner.objects.create(**podcast_owner)
        podcast.owner=owner
        podcast.save()
        self.podcast_object=podcast
        return podcast

    def save_episode(self):
        if self.save_podcast() is not None:
            episodes=[]
            for item in self.episode_list:
                new_episode=dict(map(lambda i:(i[0].replace(',','_'),i[1]),item.items()))
                image=Image.objects.create(url=new_episode.pop('itunes_image'))
                episode=Episode.objects.create(itunes_image=image,podcast=self.podcast_object,**new_episode)
                episodes.append(episode)
            return episodes
        return None
        
            
            
                                
# p=XMLParser(r'C:\Users\Lenovo\Desktop\Podcast Project\config\feeds.xml')
# print(p.save_podcast())

    




  


