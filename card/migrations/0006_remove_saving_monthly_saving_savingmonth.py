# Generated by Django 4.2 on 2025-03-28 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0005_alter_transaction_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saving',
            name='monthly_saving',
        ),
        migrations.CreateModel(
            name='SavingMonth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('year', models.PositiveIntegerField()),
                ('month', models.PositiveIntegerField()),
                ('is_paid', models.BooleanField(default=False)),
                ('saving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_savings', to='card.saving')),
            ],
        ),
    ]
