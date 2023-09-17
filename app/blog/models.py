from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model
# from app.authorization.models import CustomUser
# import sys
# sys.path.insert(0, '/app/')
# from app.authorization.models import CustomUser
import os
os.path.join("C:/Users/tvtes/AppData/Local/Programs/Python/Захист_Проєкту2024/app")


from authorization.models import CustomUser

User = get_user_model()
# Create your models here.
class Tags(models.Model):
    name_of_topic = models.TextField(max_length=34)

    def __str__(self):
        return self.name_of_topic

class Articles(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_id_number = models.IntegerField()
    title = models.TextField(max_length=56)
    content = models.TextField()
    picture_url = models.TextField()
    tags = ArrayField(models.TextField(default="No tags added"), default=list)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = ArrayField(models.IntegerField(default=0), default=list)
    dislikes = ArrayField(models.IntegerField(default=0), default=list)


    def to_like(self, user_id):
        if user_id not in self.likes:
            if user_id in self.dislikes:
                self.dislikes.remove(user_id)
            self.likes.append(user_id)
            self.save()

    def to_dislike(self, user_id):
        if user_id not in self.dislikes:
            if user_id in self.likes:
                self.likes.remove(user_id)
            self.dislikes.append(user_id)
            self.save()

    def add_tag(self, tag):
        self.tags.append(tag)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    # reputation = models.IntegerField()
    # questions = models.IntegerField()
    # answers = models.IntegerField()

class Comments_layer1(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Comments_layer2(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    comment = models.ForeignKey(Comments_layer1, on_delete=models.CASCADE)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Feedbacks(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    number_of_stars = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.number_of_stars)




