from django.db import models

# Create your models here.


class Server(models.Model):
    language = models.CharField(max_length=2)
    version = models.CharField(max_length=3)
    ip = models.IPAddressField()
    port = models.IntegerField(max_length=5)

    class Meta:
        unique_together = ['language', 'version']