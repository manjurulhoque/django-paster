from django.conf import settings
from django.db import models
from django.utils import timezone


class Syntax(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True)
    extension = models.CharField(max_length=20, blank=True)
    active = models.BooleanField(default=True)
    popular = models.BooleanField(default=True)


class Paste(models.Model):
    title = models.CharField(max_length=100, blank=True)
    slug = models.CharField(unique=True, max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, default=None, blank=True, null=True,
                             related_name='pastes')
    content = models.TextField()
    syntax = models.CharField(max_length=20)
    expire_time = models.DateTimeField(blank=True, default=None)
    expire = models.CharField(blank=True, max_length=20)
    status = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0, blank=True)
    self_destroy = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def content_size(self):
        return "{:10.2f}".format((len(self.content) / 1000))

    @property
    def language(self):
        return self.syntax

    def language_syntax(self):
        try:
            return Syntax.objects.get(slug=self.syntax)
        except Syntax.DoesNotExist:
            return None
