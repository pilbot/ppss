from django.db.models import Model
from django.db.models.fields import IntegerField, CharField, DateField, URLField
from django.db.models.fields.related import ForeignKey

from cards.fields import CountryField
from django.db.models.fields.files import ImageField

class Location(Model):
    name = CharField(max_length=30)


class Condition(Model):
    name = CharField(max_length=30)


class Variant(Model):
    name = CharField(max_length=30)


class Rarity(Model):
    name = CharField(max_length=30)
    logo = ImageField(upload_to='rarity', null=True, blank=True)

    def __unicode__(self):
        """
        The string representation of the rarity.
        """
        return self.name


class CardType(Model):
    name = CharField(max_length=30)
    logo = ImageField(upload_to='type', null=True, blank=True)

    def __unicode__(self):
        """
        The string representation of the card type.
        """
        return self.name

class CardSet(Model):

    class Meta:
        ordering = ["set_no"]

    set_no = IntegerField(blank=True, null=True)
    country = CountryField()
    name = CharField(max_length=255, blank=True)
    release = DateField(blank=True, null=True)
    logo = ImageField(upload_to='set', null=True, blank=True)
    partial_url = CharField(max_length=255, blank=True)
    official_count = IntegerField(blank=True, null=True)

    def __unicode__(self):
        """
        The string representation of the card set.
        """
        return self.name 

class Card(Model):

    class Meta:
        ordering = ["card_no"]

    card_no = IntegerField(blank=True, null=True)
    card_set = ForeignKey(CardSet)
    name = CharField(max_length=255)
    url = URLField()
    card_type = ForeignKey(CardType)
    rarity = ForeignKey(Rarity)


class CardInstance(Model):
    card = ForeignKey(Card)
    variant = ForeignKey(Variant)
    location = ForeignKey(Location)
    condition = ForeignKey(Condition)

