from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Paiement
from .serializers import PaiementSerializer, EcheanceDetailSerializer
from credits.models import EcheanceRemboursement, DemandeCredit

class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['agent', 'admin']

class EnregistrerPaiementView(generics.CreateAPIView):
    serializer_class = PaiementSerializer
    permission_classes = [IsAgent]

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user)

class HistoriquePaiementsView(generics.ListAPIView):
    serializer_class = PaiementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Paiement.objects.filter(echeance__demande__client=user)
        return Paiement.objects.all()

class EcheancesParCreditView(generics.ListAPIView):
    serializer_class = EcheanceDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        credit_id = self.kwargs['credit_id']
        user = self.request.user
        if user.role == 'client':
            return EcheanceRemboursement.objects.filter(
                demande__id=credit_id,
                demande__client=user
            )
        return EcheanceRemboursement.objects.filter(demande__id=credit_id)