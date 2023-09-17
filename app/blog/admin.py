from django.contrib import admin
from .models import Articles, Tags, Comments_layer1, Comments_layer2, Feedbacks
# Register your models here.

admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Comments_layer1)
admin.site.register(Comments_layer2)
admin.site.register(Feedbacks)
