from django.urls import path
from django.urls import include, re_path
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/favicon.png', permanent=True)

from . import views

urlpatterns = [
	path('favicon.ico', favicon_view, name='favicon'),
	path('', views.index, name='index'),
	path('actualizar_estado', views.actualizar_estado, name='actualizar_estado'),
	path('server', views.server, name='server'),
	path('actualizarServer', views.actualizarServer, name='actualizarServer'),

]