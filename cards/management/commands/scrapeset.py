import json
import re

from urllib2 import urlopen
from urlparse import urlparse

from django.core.files.base import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand, CommandError
from django.utils.http import urlquote
from bs4 import BeautifulSoup

from cards.models import CardSet, Card, Rarity, CardType
from bs4.element import NavigableString



BASE_URL = "http://bulbapedia.bulbagarden.net/{0}"
API_URL = "w/api.php?format=json&action=parse&prop=text&page={0}"

NO_CARDSETS = "no cardsets in database, please run manage.py scrapesets\n"
NO_SETS_FOUND = "could not find set {0}, valid options are: \n{1}"
FOUND_CS = "found card sets {0}"

CARD_TYPE_MAP = {
    "I": "Item",
    "St": "Stadium",
    "Su": "Supporter",
    "T": "Trainer"
}

class Command(BaseCommand):
    args = "<set name>"

    def handle(self, *args, **options):
        all_sets = CardSet.objects.all()

        if len(all_sets) == 0:
            raise CommandError(NO_CARDSETS)

        if len(args) == 1:
            sets = CardSet.objects.filter(name__icontains=args[0],
                country="GB")
            if len(sets) < 1:
                raise CommandError(NO_SETS_FOUND.format(args[0],
                    "\n".join([str(cs) for cs in all_sets])))
        else:
            sets = CardSet.objects.filter(country="GB")

        self.stdout.write("found card sets {0}\n".format(
            ", ".join([str(cs) for cs in sets])))
        self.stdout.write("Started Scrape command\n")

        card_no = re.compile("\s*(?P<card_no>\d+)/(?P<count>\d+)\s*")
        card_list_h2 = re.compile("((C|c)ard (L|l)ist(s)*)|(Setlist)")
        energy_type = re.compile(
            "(?P<energy_type>\w+) Energy \(((TCG)|(Basic))\)")

        for cs in sets:
            self.stdout.write("Processing '{0}'\n".format(cs.name))

            if cs.partial_url is None or cs.partial_url == "":
                raise CommandError("{0} does not have a valid URL".format(cs))

            html = json.load(urlopen(
                BASE_URL.format(
                    API_URL.format(
                        urlquote(cs.partial_url)))))['parse']['text']['*']
            try:
                h2 = (node
                      for node in BeautifulSoup(html).find_all("h2")
                      if node.find("span", "mw-headline") != None and
                          node.find(text=card_list_h2) != None).next()
                rows = (node.find_all("tr")
                       for node in h2.next_siblings
                       if not isinstance(node, NavigableString) and
                           node.find("b") != None and
                           node.find("b").find(text=cs.name) != None).next()
            except StopIteration:
                self.stdout.write(
                    "'{0}' does not have any valid cards\n".format(cs.name))
                continue

            cs.card_set.all().delete()

            for tr in rows:
                td = tr.find("td")
                if td is not None and td != -1:
                    match = card_no.match(td.text)
                    if match != None \
                        and int(match.group("count")) == cs.official_count:

                        node = td.next_sibling.next_sibling
                        name_node = node.next_sibling.next_sibling
                        type_node = name_node.next_sibling.next_sibling
                        rarity_node = type_node.next_sibling.next_sibling

                        if rarity_node.a is None and rarity_node.a != -1:
                            rarity_name = "None"
                        else:
                            rarity_name = rarity_node.a['title'].strip()

                        rarity, created = Rarity.objects.get_or_create(
                            name=rarity_name)

                        if created and rarity_node.a != None \
                            and rarity_node.a.img != None:

                            logo_temp = NamedTemporaryFile()
                            rarity_url = rarity_node.a.img['src']
                            logo_temp.write(urlopen(rarity_url).read())
                            logo_ext = urlparse(rarity_url).path.split('.')[-1]
                            logo_filename="{0}.{1}".format(str(rarity.id),
                                logo_ext)
                            logo_temp.flush()
                            rarity.logo.save(logo_filename, File(logo_temp))

                        if type_node.a is not None and type_node.a != -1:
                            card_type_name = type_node.a['title'].strip()
                            t_match = energy_type.match(card_type_name)
                            if t_match != None:
                                card_type_name = t_match.group("energy_type")
                        elif type_node.img is not None and type_node.img != -1 \
                            and type_node.img['alt'] == "Dragon-attack.png":
                            card_type_name = "Dragon"
                        else:
                            try:
                                card_type_name = CARD_TYPE_MAP[
                                    type_node.text.strip()]
                            except KeyError:
                                self.stderr.write(
                                    "Unrecognised type {0}".format(
                                    str(type_node)))

                        card_type, created =  CardType.objects.get_or_create(
                            name=card_type_name)

                        if created and type_node.a != None \
                            and type_node.a.img != None:

                            logo_temp = NamedTemporaryFile()
                            card_type_url = type_node.a.img['src']
                            logo_temp.write(urlopen(card_type_url).read())
                            logo_ext = urlparse(card_type_url
                                ).path.split('.')[-1]
                            logo_filename="{0}.{1}".format(str(card_type.id),
                                    logo_ext)
                            logo_temp.flush()
                            card_type.logo.save(logo_filename, File(logo_temp))

                        card = Card(card_no=match.group("card_no"),
                            card_set=cs,
                            name=name_node.text.encode('utf-8').strip(),
                            card_type=card_type, rarity=rarity)

                        if name_node.a is not None and name_node.a != -1:
                            card.url = BASE_URL.format(name_node.a['href'])

                        card.save()
                        self.stdout.write("{0}/{1} - {2} ({3})\n".format(
                            str(card.card_no), str(cs.official_count),
                            card.name, cs.name))

            self.stdout.write("total cards {0}\n".format(
                str(cs.card_set.all().count())))

