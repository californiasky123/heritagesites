from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('sites/', views.SiteListView.as_view(), name='sites'),
    path('sites/<int:pk>/', views.SiteDetailView.as_view(), name='site_detail'),
    path('countries/', views.CountryAreaListView.as_view(), name='country_area'), # added during midterm 10/23  #debugging #tried changing this to country_areas during debugging 11/8/18 hw8
    path('country/<int:pk>/', views.CountryAreaDetailView.as_view(), name='country_area_detail'), #added during midterm 10/23
    path('sites/new/', views.SiteCreateView.as_view(), name='site_new'), #chnote added 11/8 during hw8
    path('sites/<int:pk>/delete/', views.SiteDeleteView.as_view(), name='site_delete'), #chnote added 11/8 during hw8
path('sites/<int:pk>/update/', views.SiteUpdateView.as_view(), name='site_update'), #chnote added 11/8 during hw8
]

#chnote: created 10/10/2018 from starter code