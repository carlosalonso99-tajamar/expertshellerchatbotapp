from django.contrib import admin
from .models import GeneratedJSON
# Register your models here.

admin.site.site_header = "Expert Sheller Chatbot"
#Model registering
admin.site.register(GeneratedJSON)