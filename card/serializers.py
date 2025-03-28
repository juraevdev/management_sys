from rest_framework import serializers
from card.models import Card, Saving, Transaction

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"

    def create(self, validated_data):
        card = Card.objects.create(**validated_data)
        return card


class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = "__all__"

    def create(self, validated_data):
        saving = Saving.objects.create(**validated_data)
        return saving


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        transacton = Transaction.objects.create(**validated_data)
        return transacton


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