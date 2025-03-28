from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.timezone import now, timedelta, make_aware, datetime
from card.models import Card, Saving, Transaction
from card.serializers import (
    CardSerializer,
    SavingSerializer,
    TransactionSerializer,
    TransactionExpenseSerializer,
    TransactionIncomeSerializer
)

class CardApiView(generics.GenericAPIView):
    serializer_class = CardSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        cash_amount = request.data.get("cash", 0)

        card, created = Card.objects.get_or_create(
            user=user,
            defaults={"cash": cash_amount}
            )

        if not created:
            return Response({'message': 'Sizda allaqachon karta mavjud'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(card)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    

class CardGetApiView(generics.GenericAPIView):
    serializer_class = CardSerializer
    queryset = Card.objects.all()

    def get(self, request):
        cards = Card.objects.filter(user=request.user)
        serializer = self.get_serializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class SavingApiView(generics.GenericAPIView):
    serializer_class = SavingSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        card = Card.objects.filter(user=user).first() 

        if not card:  
            return Response({"error": "Sizda karta mavjud emas!"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()  
        data["card"] = card.id  
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'Saving created successfully!'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class SavingGetApiView(generics.GenericAPIView):
    serializer_class = SavingSerializer
    queryset = Saving.objects.all()

    def get(self, request):
        savings = Saving.objects.filter(card__user=request.user, paid=False)
        serializer = self.get_serializer(savings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# class TransactionApiView(generics.GenericAPIView):
#     serializer_class = TransactionSerializer

#     def post(self, request, *args, **kwargs):
#         serialzier = self.get_serializer(data=request.data)
#         if serialzier.is_valid(raise_exception=True):
#             transaction = serialzier.save(user=request.user)
#             total_today = transaction.calculate()
#             return Response({
#                 'message': 'Transaction saved',
#                 'total_today': total_today,
#             }, status=status.HTTP_201_CREATED)
#         return Response(serialzier.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TransactionListApiView(generics.GenericAPIView):
    serializer_class = TransactionSerializer

    def get(self, request):
        user = request.user
        transaction = Transaction.objects.all()
        serializer = self.get_serializer(transaction, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TransactionExpenseApiView(generics.GenericAPIView):
    serializer_class = TransactionExpenseSerializer

    def post(self, request, *args, **kwargs):
        user = request.user

        try: 
            card = Card.objects.get(user=user)
        except Card.DoesNotExist:
            return Response({'message': 'Bank account not found!'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['category'] = 'expense'

        serializer = self.get_serializer(data=data, context={'user': user})
        if serializer.is_valid(raise_exception=True):
            expense_amount = serializer.validated_data['amount']
            with transaction.atomic():
                card.cash -= expense_amount
                card.save()
                serializer.save() 

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class TransactionIncomeApiView(generics.GenericAPIView):
    serializer_class = TransactionIncomeSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            card = Card.objects.get(user=user)
        except Card.DoesNotExist:
            return Response({'message': 'Bank account not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        data['category'] = 'income'
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            expense_amount = serializer.validated_data['amount']
            with transaction.atomic():
                card.cash += expense_amount
                card.save()
                serializer.save(user=user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
