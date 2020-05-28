from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    status = models.IntegerField(default=0, null=False)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "users"