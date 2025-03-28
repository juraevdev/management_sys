from django.db import models
from accounts.models import CustomUser
from django.utils.timezone import now

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
    paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk: 
            super().save(*args, **kwargs)
            self.create_monthly_savings()
        else:
            super().save(*args, **kwargs)

    def create_monthly_savings(self):
        if self.duration_months > 0:
            monthly_amount = self.target_amount / self.duration_months
            for i in range(self.duration_months):
                month = now().month + i
                year = now().year + (month // 12)
                month = (month % 12) or 12
                SavingMonth.objects.create(saving=self, amount=monthly_amount, year=year, month=month)


class SavingMonth(models.Model):
    saving = models.ForeignKey(Saving, on_delete=models.CASCADE, related_name="monthly_savings")
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)



class TransactionCategory(models.TextChoices):
    INCOME = 'income', 'Kirim'
    EXPENSE = 'expense', 'Chiqim'


class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    category = models.CharField(max_length=10, choices=TransactionCategory.choices)
    description = models.TextField(null=True, blank=True)
