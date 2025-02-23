from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Register permissions so they can be managed in Django Admin
# admin.site.register(Permission)
# admin.site.register(ContentType)


admin.site.register(Conversation)
# Register your models here.
admin.site.site_title='ephraim websockets'
admin.site.index_title='ephraim websockets'
admin.site.site_header='ephraim websockets'

@admin.register(ConversationMessage)
class Adminmes(admin.ModelAdmin):
    list_display = ['id','body','sent_to','created_by']

