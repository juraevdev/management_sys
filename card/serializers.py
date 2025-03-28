from rest_framework import serializers
from card.models import Card, Saving, SavingMonth, Transaction

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

    def create(self, validated_data):
        card = Card.objects.create(**validated_data)
        return card


class SavingMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingMonth
        fields = ["id", "amount", "year", "month", "is_paid"]

class SavingSerializer(serializers.ModelSerializer):
    monthly_savings = SavingMonthSerializer(many=True, read_only=True)

    class Meta:
        model = Saving
        fields = ["id", "name", "target_amount", "duration_months", "paid", "monthly_savings"]



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction


class TransactionIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def get_date(self, obj):
        return obj.date.strftime('%m.%d.%Y')
    
    def create(self, validated_data):
        transacton = Transaction.objects.create(**validated_data)
        return transacton


class TransactionExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def get_date(self, obj):
        return obj.date.strftime('%m.%d.%Y')
    
    def create(self, validated_data):
        user = self.context['user']
        transacton = Transaction.objects.create(user=user, **validated_data)
        return transacton