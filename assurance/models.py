from django.db import models
from accounts.models import User

class ProduitAssurance(models.Model):
    TYPE_CHOICES = [
        ('vie', 'Assurance Vie'),
        ('deces_invalidite', 'Décès-Invalidité'),
    ]
    nom = models.CharField(max_length=100)
    type_assurance = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    prix_mensuel = models.DecimalField(max_digits=10, decimal_places=2)
    est_actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} ({self.type_assurance})"


class SouscriptionAssurance(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='souscriptions')
    produit = models.ForeignKey(ProduitAssurance, on_delete=models.CASCADE, related_name='souscriptions')
    date_souscription = models.DateField(auto_now_add=True)
    date_expiration = models.DateField()
    est_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.client.username} - {self.produit.nom}"