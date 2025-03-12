from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world, name='hello-world'),
    path('stock-price/', views.get_stock_price_view, name='stock-price'),
    path('market-cap/', views.get_market_cap_view, name='market_cap'),
    path('pe-ratio/', views.get_pe_ratio_view, name='pe_ratio'),
]