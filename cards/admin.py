from django.contrib import admin

from cards.models import Rarity, Variant, CardType, CardSet, Card, CardInstance

admin.site.register(Rarity)
admin.site.register(Variant)
admin.site.register(CardType)
admin.site.register(CardSet)
admin.site.register(Card)
admin.site.register(CardInstance)

