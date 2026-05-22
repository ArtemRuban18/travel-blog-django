from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "content_id")

    def __str__(self):
        return self.user.username
    
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "content_id"]),
        ]
        constraints = [
        models.UniqueConstraint(
            fields=["user", "content_type", "content_id"],
            name="unique_like"
            )
        ]
        verbose_name = "Like"
        verbose_name_plural = "Likes"