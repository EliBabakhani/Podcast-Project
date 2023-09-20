from django.db import models

class Podcast(models.Model):
    title = models.CharField(max_length=200)
    generator = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    copyright = models.CharField(max_length=200, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    link=models.CharField(max_length=100, null=True, blank=True)
    pubDate=models.CharField(max_length=50, null=True, blank=True)#edit to datefield
    itunes_summary = models.CharField(max_length=200, null=True, blank=True)
    itunes_type = models.CharField(max_length=50, null=True, blank=True)
    itunes_explicit = models.CharField(max_length=50, null=True, blank=True)
    itunes_author = models.ForeignKey('Author', on_delete=models.CASCADE, null=True, blank=True)
    itunes_category = models.CharField(max_length=100, null=True, blank=True)
    managingEditor = models.CharField(max_length=100, null=True, blank=True)
    owner=models.ForeignKey('Owner', on_delete=models.CASCADE, null=True, blank=True)
    image=models.ForeignKey('Image', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    pubDate = models.CharField(null=True, blank=True)
    itunes_image=models.ForeignKey('Image', on_delete=models.CASCADE, null=True, blank=True)
    author=models.CharField(max_length=100, null=True, blank=True)
    itunes_episodeType=models.CharField(max_length=50, null=True, blank=True)
    itunes_summary=models.TextField( null=True, blank=True)
    guid=models.CharField(max_length=200, null=True, blank=True)
    itunes_explicit=models.CharField(max_length=500, null=True, blank=True)
    itunes_keywords=models.TextField(null=True, blank=True)
    itunes_duration=models.CharField(max_length=50, null=True, blank=True)
    content_encoded=models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
