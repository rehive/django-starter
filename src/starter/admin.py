from django.contrib import admin

from starter.models import Message


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)


class MessageAdmin(CustomModelAdmin):
    pass


class WebhookAdmin(CustomModelAdmin):
    pass

admin.site.register(Message, MessageAdmin)

