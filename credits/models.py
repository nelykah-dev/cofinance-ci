from django.db import models
from accounts.models import User

class DemandeCredit(models.Model):
    STATUT_CHOICES = [
        ('soumise', 'Soumise'),
        ('en_analyse', 'En analyse'),
        ('approuvee', 'Approuvée'),
        ('decaissee', 'Décaissée'),
        ('rejetee', 'Rejetée'),
    ]

    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_credit')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='dossiers_traites')
    montant_demande = models.DecimalField(max_digits=12, decimal_places=2)
    duree_mois = models.PositiveIntegerField()
    motif = models.TextField()
    piece_justificative = models.FileField(upload_to='pieces/', blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='soumise')
    score_eligibilite = models.IntegerField(default=0)
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    date_soumission = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def calculer_score(self):
        score = 50
        if self.montant_demande <= 100000:
            score += 20
        elif self.montant_demande <= 500000:
            score += 10
        if self.duree_mois <= 12:
            score += 15
        elif self.duree_mois <= 24:
            score += 5
        if self.client.credits_rembourses if hasattr(self.client, 'credits_rembourses') else False:
            score += 15
        self.score_eligibilite = min(score, 100)
        return self.score_eligibilite

    def __str__(self):
        return f"Crédit {self.id} - {self.client.username} - {self.statut}"


class EcheanceRemboursement(models.Model):
    demande = models.ForeignKey(DemandeCredit, on_delete=models.CASCADE, related_name='echeances')
    numero = models.PositiveIntegerField()
    date_echeance = models.DateField()
    montant_principal = models.DecimalField(max_digits=12, decimal_places=2)
    montant_interet = models.DecimalField(max_digits=12, decimal_places=2)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2)
    est_paye = models.BooleanField(default=False)

    def __str__(self):
        return f"Échéance {self.numero} - Crédit {self.demande.id}"