from django.conf.urls import include, url
#from views.main import main
from main import *


urlpatterns = [		
    url(r'^main/$', main, name='main'),
    url(r'^configure/$', configure),
    url(r'^load_summary/$', load_summary),
    url(r'^load_result/$', load_result),
    url(r'^asign_label/$', asign_label),    
    url(r'^cantidad_grupo/$', cantidad_grupo),
    url(r'^resumen/$', resumen),
    url(r'^load_resumen/$', load_resumen),
    url(r'^detalle_vuelo/(?P<flight>.+)/$', detalle_vuelo),
    url(r'^load_detalle_vuelo/$', load_detalle_vuelo),
]
