import json
import re

from datetime import datetime
from urllib2 import urlopen

from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from bs4 import BeautifulSoup

from cards.models import CardSet
from urlparse import urlparse


BASE_URL = "http://bulbapedia.bulbagarden.net/w/api.php?format=json&action=parse&prop=text&page={0}"
CARDSET_PAGE = "List_of_Pok%C3%A9mon_Trading_Card_Game_expansions"

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("start scraping from Bulbapedia...\n")
        p = re.compile("official (count|total) (?P<count>\d+)")

        CardSet.objects.all().delete()

        html = json.load(urlopen(BASE_URL.format(CARDSET_PAGE))
            )['parse']['text']['*']
        set_tbl = BeautifulSoup(html).find("table").find(
            "table").find_all("tr")[1:]

        for r in set_tbl:
            data = r.find_all("td")
            logo_temp = NamedTemporaryFile()

            try:
                eng_cs = CardSet(country="GB")
                eng_cs.set_no = int(r.find("th").text.strip())
                eng_cs.name = data[2].text.strip()
                try:
                    logo_url = data[1].a.img['src']
                    logo_temp.write(urlopen(logo_url).read())
                    logo_ext = urlparse(logo_url).path.split('.')[-1]
                    logo_filename="{0}_{1}.{2}".format(eng_cs.country,
                        eng_cs.set_no, logo_ext)
                    logo_temp.flush()
                    eng_cs.logo.save(logo_filename, File(logo_temp))
                except (TypeError, AttributeError):
                    pass
                try:
                    eng_cs.partial_url = data[2].a['title']
                except TypeError:
                    pass
                eng_cs.release = datetime.strptime(data[6].text.strip(),
                    "%B %d, %Y")
                count = data[4].find("span", "explain")
                try:
                    eng_cs.official_count = int(p.search(count['title']
                                                         ).group("count"))
                except (TypeError, AttributeError):
                    if data[4].text.strip() != "":
                        eng_cs.official_count = int(data[4].text.strip())

                self.stdout.write("scraped: {0}\n".format(eng_cs))
                eng_cs.save()
            except ValueError:
                # If there is no valid set_no
                pass

            try:
                jap_cs = CardSet(country="JP")
                jap_cs.set_no = int(data[0].text.strip())
                jap_cs.name = data[3].text.strip()
                try:
                    logo_url = data[1].a.img['src']
                    logo_temp.write(urlopen(logo_url).read())
                    logo_ext = urlparse(logo_url).path.split('.')[-1]
                    logo_filename="{0}_{1}.{2}".format(jap_cs.country,
                        jap_cs.set_no, logo_ext)
                    logo_temp.flush()
                    jap_cs.logo.save(logo_filename, File(logo_temp))
                except (TypeError, AttributeError):
                    pass
                try:
                    jap_cs.partial_url = data[2].a['title']
                except TypeError:
                    pass
                jap_cs.release = datetime.strptime(data[7].text.strip(),
                    "%B %d, %Y")
                count = data[5].find("span", "explain")
                try:
                    jap_cs.official_count = int(p.search(count['title']
                                                         ).group("count"))
                except (TypeError, AttributeError):
                    if data[5].text.strip() != "":
                        jap_cs.official_count = int(data[5].text.strip())

                self.stdout.write("scraped: {0}\n".format(jap_cs))
                jap_cs.save()
            except ValueError:
                # If there is no valid set_no
                pass

        self.stdout.write("total sets {0}\n".format(
            str(CardSet.objects.all().count())))

