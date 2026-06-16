from rest_framework import serializers
from .models import ProduitAssurance, SouscriptionAssurance
from datetime import date
from dateutil.relativedelta import relativedelta

class ProduitAssuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitAssurance
        fields = '__all__'

class SouscriptionSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(read_only=True)
    produit_detail = ProduitAssuranceSerializer(source='produit', read_only=True)
    jours_avant_expiration = serializers.SerializerMethodField()

    class Meta:
        model = SouscriptionAssurance
        fields = '__all__'
        read_only_fields = ['client', 'date_souscription', 'est_active']

    def get_jours_avant_expiration(self, obj):
        delta = obj.date_expiration - date.today()
        return delta.days

    def create(self, validated_data):
        request = self.context['request']
        validated_data['client'] = request.user
        if 'date_expiration' not in validated_data:
            validated_data['date_expiration'] = date.today() + relativedelta(months=1)
        return super().create(validated_data)