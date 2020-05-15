from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=16)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=300)
    follow = models.ManyToManyField(
        'self', through='Follow', symmetrical=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'accounts'


class Follow(models.Model):  # model to describe the follow-following relationship
    from_user = models.ForeignKey(
        'Account', on_delete=models.SET_NULL, null=True, related_name='from_user')
    to_user = models.ForeignKey(
        'Account', on_delete=models.SET_NULL, null=True, related_name='to_user')

    class Meta:
        db_table = 'follows'
