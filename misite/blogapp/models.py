from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name='article')
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name='article')
    tags = models.ManyToManyField(to=Tag, related_name='article')

    def __str__(self):
        return self.title