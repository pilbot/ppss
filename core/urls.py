from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from core.settings import MEDIA_URL, MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^set/(\d+)/', 'cards.views.set_list'),
    url(r'^card/(\d+)/new/', 'cards.views.new_cardinstance'),
    url(r'^card/(\d+)/', 'cards.views.card_detail'),
    url(r'^cardinstance/(\d+)/delete/', 'cards.views.delete_cardinstance'),
    url(r'^cardinstance/(\d+)/', 'cards.views.edit_cardinstance'),

    url(r'^$', 'cards.views.index'),
) + static(MEDIA_URL, document_root=MEDIA_ROOT)

