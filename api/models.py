from django.db import models

# Create your models here.
class ScrapedData(models.Model):
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=225)
    content = models.TextField()
    ScrapedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ' - ' + self.url