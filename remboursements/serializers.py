from rest_framework import serializers
from .models import Paiement
from credits.models import EcheanceRemboursement

class PaiementSerializer(serializers.ModelSerializer):
    agent = serializers.StringRelatedField(read_only=True)
    echeance = serializers.PrimaryKeyRelatedField(queryset=EcheanceRemboursement.objects.all())

    class Meta:
        model = Paiement
        fields = '__all__'
        read_only_fields = ['agent', 'date_paiement', 'penalite']

class EcheanceDetailSerializer(serializers.ModelSerializer):
    paiements = PaiementSerializer(many=True, read_only=True)
    jours_retard = serializers.SerializerMethodField()

    class Meta:
        model = EcheanceRemboursement
        fields = '__all__'

    def get_jours_retard(self, obj):
        from datetime import date
        if not obj.est_paye and date.today() > obj.date_echeance:
            return (date.today() - obj.date_echeance).days
        return 0