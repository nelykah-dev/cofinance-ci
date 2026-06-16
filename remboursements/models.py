from django.db import models
from accounts.models import User
from credits.models import EcheanceRemboursement

class Paiement(models.Model):
    echeance = models.ForeignKey(EcheanceRemboursement, on_delete=models.CASCADE, related_name='paiements')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='paiements_enregistres')
    montant_paye = models.DecimalField(max_digits=12, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    penalite = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    note = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        from datetime import date
        if date.today() > self.echeance.date_echeance:
            jours_retard = (date.today() - self.echeance.date_echeance).days
            self.penalite = float(self.echeance.montant_total) * 0.01 * jours_retard
        super().save(*args, **kwargs)
        self.echeance.est_paye = True
        self.echeance.save()

    def __str__(self):
        return f"Paiement échéance {self.echeance.id} - {self.montant_paye} FCFA"