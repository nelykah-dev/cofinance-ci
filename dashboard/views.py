from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from credits.models import DemandeCredit
from assurance.models import SouscriptionAssurance
from accounts.models import User

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class DashboardView(APIView):
    permission_classes = [IsAdmin]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='date_debut', type=str, required=False),
            OpenApiParameter(name='date_fin', type=str, required=False),
            OpenApiParameter(name='agent_id', type=int, required=False),
        ],
        responses={200: dict}
    )
    def get(self, request):
        date_debut = request.query_params.get('date_debut')
        date_fin = request.query_params.get('date_fin')
        agent_id = request.query_params.get('agent_id')

        credits_qs = DemandeCredit.objects.all()
        if date_debut:
            credits_qs = credits_qs.filter(date_soumission__date__gte=date_debut)
        if date_fin:
            credits_qs = credits_qs.filter(date_soumission__date__lte=date_fin)
        if agent_id:
            credits_qs = credits_qs.filter(agent__id=agent_id)

        credits_par_statut = {
            'soumise': credits_qs.filter(statut='soumise').count(),
            'en_analyse': credits_qs.filter(statut='en_analyse').count(),
            'approuvee': credits_qs.filter(statut='approuvee').count(),
            'decaissee': credits_qs.filter(statut='decaissee').count(),
            'rejetee': credits_qs.filter(statut='rejetee').count(),
        }

        total_echeances = 0
        echeances_payees = 0
        for credit in credits_qs:
            echeances = credit.echeances.all()
            total_echeances += echeances.count()
            echeances_payees += echeances.filter(est_paye=True).count()

        taux_recouvrement = (
            round((echeances_payees / total_echeances) * 100, 2)
            if total_echeances > 0 else 0
        )

        souscriptions_actives = SouscriptionAssurance.objects.filter(est_active=True).count()
        total_clients = User.objects.filter(role='client').count()
        total_agents = User.objects.filter(role='agent').count()

        return Response({
            'credits_par_statut': credits_par_statut,
            'taux_recouvrement': f"{taux_recouvrement}%",
            'souscriptions_actives': souscriptions_actives,
            'total_clients': total_clients,
            'total_agents': total_agents,
        })