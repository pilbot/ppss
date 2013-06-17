from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext

from cards.models import Rarity, CardType, CardSet

def index(request):
    data = {
        "rarities": Rarity.objects.all(),
        "types": CardType.objects.all(),
        "sets": CardSet.objects.all().order_by("country", "set_no")
    }
    
    return render_to_response("index.html", data,
        context_instance=RequestContext(request))

def set_list(request, set_id):
    cs = get_object_or_404(CardSet, pk=set_id)

    return render_to_response("set_list.html", {"set": cs},
        context_instance=RequestContext(request))

