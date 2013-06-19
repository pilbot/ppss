from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from core.settings import MEDIA_URL, MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^set/(\d+)/', 'cards.views.set_list'),

    url(r'^$', 'cards.views.index'),
) + static(MEDIA_URL, document_root=MEDIA_ROOT)

