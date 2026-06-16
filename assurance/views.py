from rest_framework import generics, permissions
from .models import ProduitAssurance, SouscriptionAssurance
from .serializers import ProduitAssuranceSerializer, SouscriptionSerializer
from datetime import date, timedelta

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class ProduitAssuranceListView(generics.ListAPIView):
    queryset = ProduitAssurance.objects.filter(est_actif=True)
    serializer_class = ProduitAssuranceSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProduitAssuranceCreateView(generics.CreateAPIView):
    queryset = ProduitAssurance.objects.all()
    serializer_class = ProduitAssuranceSerializer
    permission_classes = [IsAdmin]

class SouscriptionCreateView(generics.CreateAPIView):
    serializer_class = SouscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class MesSouscriptionsView(generics.ListAPIView):
    serializer_class = SouscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return SouscriptionAssurance.objects.filter(client=user)
        return SouscriptionAssurance.objects.all()

class SouscriptionsExpirantBientotView(generics.ListAPIView):
    serializer_class = SouscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        dans_15_jours = date.today() + timedelta(days=15)
        return SouscriptionAssurance.objects.filter(
            date_expiration__lte=dans_15_jours,
            est_active=True
        )