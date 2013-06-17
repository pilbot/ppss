from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.settings import PKM_BASEDIR

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^set/(\d+)/', 'cards.views.set_list'),

    url(r'^$', 'cards.views.index'),
)

urlpatterns += patterns('',
    (r'^(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': PKM_BASEDIR + '/media'})
)

