from django.urls import path
from . import views

urlpatterns = [
	path('', views.dipole, name='dipole'),
	path('static/src/fin_df.json', views.fin_df, name='fin_df'),
	path('icon.png', views.icon, name='icon')

]