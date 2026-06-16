from django.urls import path
from .views import MesNotificationsView, MarquerLuView, MarquerToutesLuesView

urlpatterns = [
    path('', MesNotificationsView.as_view(), name='mes-notifications'),
    path('<int:pk>/lire/', MarquerLuView.as_view(), name='marquer-lu'),
    path('tout-lire/', MarquerToutesLuesView.as_view(), name='tout-lire'),
]