from django.urls import path
from .views import (
    ProduitAssuranceListView,
    ProduitAssuranceCreateView,
    SouscriptionCreateView,
    MesSouscriptionsView,
    SouscriptionsExpirantBientotView,
)

urlpatterns = [
    path('produits/', ProduitAssuranceListView.as_view(), name='produits-list'),
    path('produits/creer/', ProduitAssuranceCreateView.as_view(), name='produit-creer'),
    path('souscrire/', SouscriptionCreateView.as_view(), name='souscrire'),
    path('mes-souscriptions/', MesSouscriptionsView.as_view(), name='mes-souscriptions'),
    path('expirant-bientot/', SouscriptionsExpirantBientotView.as_view(), name='expirant-bientot'),
]