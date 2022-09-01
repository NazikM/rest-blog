from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=120, unique=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def time_to_read(self):
        if len(self.content) < 1500:
            return "<1min"
        elif len(self.content) < 7500:
            return "<5min"
        else:
            return ">5min"


