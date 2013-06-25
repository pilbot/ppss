from django.contrib import admin

from cards.models import Location, Condition, Variant, Rarity, CardType, \
    CardSet, Card, CardInstance

admin.site.register(Location)
admin.site.register(Condition)
admin.site.register(Variant)
admin.site.register(Rarity)
admin.site.register(CardType)
admin.site.register(CardSet)
admin.site.register(Card)
admin.site.register(CardInstance)

