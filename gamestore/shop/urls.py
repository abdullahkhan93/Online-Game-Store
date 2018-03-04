from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name="shop"),
    path('<int:gameid>/', views.game, name='gamepage'),
    path('<int:gameid>/purchase/', views.purchase, name='purchase'),
    path('purchase_success/', views.purchaseSuccess, name='purchaseSuccess'),
    path('purchase_fail/', views.purchaseFail, name='purchaseFail')
]