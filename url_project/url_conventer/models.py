from django.contrib.auth.models import User
from django.db import models

class Urls(models.Model):
    original_url = models.URLField(help_text='Оригинальная ссылка')
    cut_url = models.URLField(max_length=30)
    using = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.original_url