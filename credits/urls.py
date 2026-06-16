from django.urls import path
from .views import DemandeCreditListCreateView, DemandeCreditDetailView, ChangerStatutView

urlpatterns = [
    path('', DemandeCreditListCreateView.as_view(), name='credits-list'),
    path('<int:pk>/', DemandeCreditDetailView.as_view(), name='credit-detail'),
    path('<int:pk>/statut/', ChangerStatutView.as_view(), name='credit-statut'),
]