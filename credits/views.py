from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import DemandeCredit
from .serializers import DemandeCreditSerializer
from notifications.models import Notification
import logging
logger = logging.getLogger(__name__)


class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['agent', 'admin']


class DemandeCreditListCreateView(generics.ListCreateAPIView):
    serializer_class = DemandeCreditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return DemandeCredit.objects.filter(client=user)
        return DemandeCredit.objects.all()

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class DemandeCreditDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = DemandeCreditSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return DemandeCredit.objects.filter(client=user)
        return DemandeCredit.objects.all()


class ChangerStatutView(APIView):
    permission_classes = [IsAgent]

    @extend_schema(
        request={'application/json': {'type': 'object', 'properties': {'statut': {'type': 'string'}}}},
        responses={200: DemandeCreditSerializer}
    )
    def patch(self, request, pk):
        try:
            demande = DemandeCredit.objects.get(pk=pk)
        except DemandeCredit.DoesNotExist:
            return Response({'error': 'Demande introuvable'}, status=404)
        nouveau_statut = request.data.get('statut')
        statuts_valides = ['soumise', 'en_analyse', 'approuvee', 'decaissee', 'rejetee']
        if nouveau_statut not in statuts_valides:
            return Response({'error': 'Statut invalide'}, status=400)
        demande.statut = nouveau_statut
        demande.agent = request.user
        demande.save()
        return Response(DemandeCreditSerializer(demande).data)


# --- Vue web pour l'agent (utilisée par le formulaire HTML) ---
import logging
logger = logging.getLogger(__name__)

@login_required
def changer_statut_web(request, credit_id):
    print("=== DÉBUT DE LA FONCTION ===")
    print(f"Utilisateur connecté : {request.user} (rôle : {request.user.role})")
    print(f"credit_id reçu : {credit_id}")
    
    # Vérification des droits
    if request.user.role not in ['agent', 'admin']:
        print("ERREUR : l'utilisateur n'a pas les droits")
        messages.error(request, "Vous n'avez pas les droits.")
        return redirect('/dashboard/')
    
    print("Étape 1 : droits OK, on cherche le crédit...")
    try:
        credit = DemandeCredit.objects.get(id=credit_id)
        print(f"Étape 2 : crédit trouvé ! ID={credit.id}, statut actuel={credit.statut}, client={credit.client}")
    except DemandeCredit.DoesNotExist:
        print(f"ERREUR : crédit #{credit_id} inexistant")
        messages.error(request, f"Le crédit #{credit_id} n'existe pas.")
        return redirect('/dashboard/')
    
    nouveau_statut = request.POST.get('statut')
    print(f"Étape 3 : nouveau statut reçu = {nouveau_statut}")
    
    if nouveau_statut not in ['approuvee', 'rejetee']:
        print("ERREUR : statut invalide")
        messages.error(request, "Statut invalide.")
        return redirect('/dashboard/')
    
    print("Étape 4 : mise à jour du statut...")
    credit.statut = nouveau_statut
    credit.agent = request.user
    credit.save()
    print("Étape 5 : sauvegarde OK")
    
    print("Étape 6 : création de la notification...")
    try:
        Notification.objects.create(
            utilisateur=credit.client,
            message=f"Votre demande de crédit #{credit.id} a été {nouveau_statut}."
        )
        print("Étape 7 : notification créée avec succès")
    except Exception as e:
        print(f"ERREUR lors de la création de la notification : {e}")
    
    messages.success(request, f"Demande {nouveau_statut} avec succès.")
    print("=== FIN DE LA FONCTION, retour vers dashboard ===")
    return redirect('/dashboard/')