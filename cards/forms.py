from django.forms import ModelForm, ModelChoiceField, HiddenInput

from cards.models import Card, CardInstance


class CardForm(ModelForm):
    card = ModelChoiceField(queryset=Card.objects.all(), widget=HiddenInput())

    class Meta:
        model = CardInstance

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)

        for fieldname in self.fields.keys():
            self.fields[fieldname].empty_label = None

