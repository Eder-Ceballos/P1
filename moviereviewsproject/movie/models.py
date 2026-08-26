from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    rating = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie/images/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-year']