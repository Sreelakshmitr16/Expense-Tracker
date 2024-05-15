from django.urls import path
from budget import views

urlpatterns=[
    path('transactions/add/',views.TransactionCreateView.as_view(),name='transactions-add'),
    path('transactions/all/',views.TransactionListView.as_view(),name='transaction-list'),
    path('transactions/<int:pk>/change/',views.TransactionUpdateView.as_view(),name='transaction-edit'),
    path('transactions/<int:pk>/remove/',views.TransactionDeleteView.as_view(),name='transaction-delete'),
    path('transactions/<int:pk>/',views.TransactionDetailView.as_view(),name='transaction-detail'),
    path('register/',views.SignUpView.as_view(),name='signup'),
    path('signin/',views.SignInview.as_view(),name='signin'),
    path('signout/',views.SignOutView.as_view(),name='signout')
]
