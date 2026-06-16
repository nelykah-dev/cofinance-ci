from django.urls import path
from .views import EnregistrerPaiementView, HistoriquePaiementsView, EcheancesParCreditView

urlpatterns = [
    path('paiements/', EnregistrerPaiementView.as_view(), name='enregistrer-paiement'),
    path('historique/', HistoriquePaiementsView.as_view(), name='historique-paiements'),
    path('credit/<int:credit_id>/echeances/', EcheancesParCreditView.as_view(), name='echeances-credit'),
]