from django.db import models

class Podcast(models.Model):
    title = models.CharField(max_length=200)
    generator = models.CharField(max_length=200)
    description = models.TextField()
    copyright = models.CharField(max_length=200)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Episode(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    pubDate = models.DateTimeField()

    def __str__(self):
        return self.title
