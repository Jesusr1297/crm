from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.lead_list),
    path('<int:pk>/', views.lead_detail),
    path('<int:pk>/update/', views.lead_update),
    path('create/', views.lead_create),

]
