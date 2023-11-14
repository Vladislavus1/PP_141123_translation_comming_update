from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
# class User_Profile(User):
    # about_user = models.TextField(max_length=350, default="")
    # profile_picture = models.TextField(default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRM24LrOEVSxaEXpikDYJUsVoQAujGaihu7u6JPOSViF7wFBr0HbqJnlWbjZY0W9W9RouU&usqp=CAU')
    # preferences = ArrayField(models.TextField(default="He have no preferences"), default=list)
    # subscribers = ArrayField(models.IntegerField(default=0), default=list)
    # subscriptions = ArrayField(models.IntegerField(default=0), default=list)
    # user = models.OneToOneField(User, verbose_name=('User'), related_name='settings',
    #                             auto_created=True, on_delete=models.CASCADE, parent_link=True, primary_key=True)

class CustomUser(AbstractUser):
    about_user = models.TextField(max_length=350, default="")
    profile_picture = models.TextField(default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRM24LrOEVSxaEXpikDYJUsVoQAujGaihu7u6JPOSViF7wFBr0HbqJnlWbjZY0W9W9RouU&usqp=CAU')
    preferences = ArrayField(models.TextField(default="He have no preferences"), default=list)
    subscribers = ArrayField(models.IntegerField(default=0), default=list)
    subscriptions = ArrayField(models.IntegerField(default=0), default=list)
    notifications = models.IntegerField(default=0)

    def add_preferences(self, preference):
        self.preferences.append(preference)
        self.save()

    def remove_preference(self, preference):
        self.preferences.remove(preference)
        self.save()

    def __str__(self):
        return self.username


    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

