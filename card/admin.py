from django.contrib import admin
from card.models import Card, Saving, SavingMonth, Transaction

admin.site.register(Card)
admin.site.register(Saving)
admin.site.register(SavingMonth)
admin.site.register(Transaction)