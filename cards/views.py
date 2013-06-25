from django.http import Http404
from django.db.models import Count
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.forms.formsets import formset_factory

from cards.models import Rarity, CardType, CardSet, Card, CardInstance
from cards.forms import CardForm


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


def card_detail(request, card_id=None):
    data = {
        "card": get_object_or_404(Card, pk=card_id),
        "sets": get_ordered_sets()
    }

    return render_to_response("card.html", data,
        context_instance=RequestContext(request))


def new_cardinstance(request, card_id):
    ci = CardInstance(card=get_object_or_404(Card, pk=card_id))
    data = {
        "card": ci.card,
        "sets": get_ordered_sets()
    }

    if request.method == "POST":
        form = CardForm(request.POST, instance=ci)
        if form.is_valid():
            form.save()
            return redirect('/card/{0}'.format(str(card_id)))
    else:
        form = CardForm(instance=ci)

    data['form'] = form
    return render_to_response('cardinstance.html', data,
        context_instance=RequestContext(request))


def edit_cardinstance(request, instance_id):
    ci = get_object_or_404(CardInstance, pk=instance_id)
    data = {
        "card": ci.card,
        "sets": get_ordered_sets()
    }

    if request.method == 'POST':
        form = CardForm(request.POST, instance=ci)
        if form.is_valid():
            form.save()
            return redirect('/card/{0}'.format(str(ci.card.id)))
    else:
        form = CardForm(instance=ci)

    data['form'] = form
    return render_to_response('cardinstance.html', data,
        context_instance=RequestContext(request))

