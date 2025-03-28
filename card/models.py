from django.db import models
from accounts.models import CustomUser

class Card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='card')
    cash = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self):
        return f'{self.user} hisob raqami'
    

class Saving(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='savings')
    name = models.CharField(max_length=100, null=True, blank=True)
    target_amount = models.DecimalField(decimal_places=2, max_digits=10)
    duration_months = models.PositiveIntegerField()
    monthly_saving = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.duration_months = int(self.duration_months)  
        if self.duration_months > 0:
            self.monthly_saving = self.target_amount / self.duration_months
        super().save(*args, **kwargs)


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.CharField(max_length=255, choices=[('income', 'Kirim'), ('expense', 'Chiqim')])
    description = models.TextField(null=True, blank=True)


