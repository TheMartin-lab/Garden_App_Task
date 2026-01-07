from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Vendor URLs
    path('my-stores/', views.my_stores, name='my_stores'),
    path('my-stores/add/', views.add_store, name='add_store'),
    path('my-stores/<int:store_id>/edit/', views.edit_store, name='edit_store'),
    path('my-stores/<int:store_id>/delete/', views.delete_store, name='delete_store'),
    path('my-stores/<int:store_id>/products/', views.store_products, name='store_products'),
    path('my-stores/<int:store_id>/products/add/', views.add_product, name='add_product'),
    path('my-stores/<int:store_id>/products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('my-stores/<int:store_id>/products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('my-stores/<int:store_id>/products/<int:product_id>/inventory/', views.adjust_inventory, name='adjust_inventory'),
    path('my-stores/<int:store_id>/products/<int:product_id>/price/', views.adjust_price, name='adjust_price'),

    # Buyer URLs
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
]
