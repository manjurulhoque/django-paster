from django.db import models


class PasteManager(models.Manager):
    def get_content_size(self):
        pass
