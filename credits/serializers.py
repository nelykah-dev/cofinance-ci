from rest_framework import serializers
from .models import DemandeCredit, EcheanceRemboursement
from datetime import date
from dateutil.relativedelta import relativedelta

class EcheanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcheanceRemboursement
        fields = '__all__'

class DemandeCreditSerializer(serializers.ModelSerializer):
    echeances = EcheanceSerializer(many=True, read_only=True)
    client = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DemandeCredit
        fields = '__all__'
        read_only_fields = ['client', 'statut', 'score_eligibilite', 'date_soumission', 'date_mise_a_jour']

    def create(self, validated_data):
        request = self.context['request']
        demande = DemandeCredit(**validated_data)
        demande.client = request.user
        demande.calculer_score()
        demande.save()
        self._generer_echeancier(demande)
        return demande

    def _generer_echeancier(self, demande):
        montant = float(demande.montant_demande)
        duree = demande.duree_mois
        taux_mensuel = float(demande.taux_interet) / 100 / 12
        if taux_mensuel > 0:
            mensualite = montant * taux_mensuel / (1 - (1 + taux_mensuel) ** -duree)
        else:
            mensualite = montant / duree
        solde = montant
        for i in range(1, duree + 1):
            interet = solde * taux_mensuel
            principal = mensualite - interet
            solde -= principal
            EcheanceRemboursement.objects.create(
                demande=demande,
                numero=i,
                date_echeance=date.today() + relativedelta(months=i),
                montant_principal=round(principal, 2),
                montant_interet=round(interet, 2),
                montant_total=round(mensualite, 2),
            )
class CreditSerializer(serializers.ModelSerializer):
    client_username = serializers.CharField(source='client.username', read_only=True)
    # ...
    class Meta:
        fields = ['id', 'client', 'client_username', 'montant_demande', ...]