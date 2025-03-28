from django.urls import path
from card.views import (
    CardApiView, CardGetApiView,
    SavingApiView,SavingGetApiView,
    TransactionListApiView,
    TransactionExpenseApiView, TransactionIncomeApiView
    # TransactionApiView,
)

urlpatterns = [
    path('create/', CardApiView.as_view()),
    path('list/', CardGetApiView.as_view()),
    path('saving/', SavingApiView.as_view()),
    path('saving/list/', SavingGetApiView.as_view()),
    # path('transaction/', TransactionApiView.as_view()),
    path('transaction/list/', TransactionListApiView.as_view()),
    path('transaction/expense/', TransactionExpenseApiView.as_view()),
    path('transaction/income/', TransactionIncomeApiView.as_view()),
]