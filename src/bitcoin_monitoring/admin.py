from django.contrib import admin

from bitcoin_monitoring.models import Transaction, Webhook


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(CustomModelAdmin, self).__init__(model, admin_site)


class TransactionAdmin(CustomModelAdmin):
    pass


class WebhookAdmin(CustomModelAdmin):
    pass

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Webhook, WebhookAdmin)
