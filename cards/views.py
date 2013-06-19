from django.db.models import Count
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext

from cards.models import Rarity, CardType, CardSet

def get_ordered_sets():
    return CardSet.objects.annotate(card_count=Count('card')
        ).filter(card_count__gte=1).order_by("country", "-set_no")

def index(request):
    cs = CardSet.objects.all()[0]
    return redirect("set/{0}/".format(cs.id), permenant=True)

def set_list(request, set_id=None):
    data = {
        "set": get_object_or_404(CardSet, pk=set_id),
        "sets": get_ordered_sets()
    }

    return render_to_response("card_list.html", data,
        context_instance=RequestContext(request))

