from django.db import models
from unidecode import unidecode
from django.template.defaultfilters import slugify


class Category(models.Model):

    title = models.CharField(max_length=30)

    description = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


        # if self.slug is None or self.slug == '': # if not commented the slug will not change when edit the category title
        self.slug = slugify(f'{unidecode(self.title)}-{self.id}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
