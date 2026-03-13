from django.urls import path
from .import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sell/', views.sell_part, name='sell'),
    #path('shop/', views.shop, name='shop'),
    path('my-products/', views.my_products, name='my_products'),
    path('delete-product/<int:item_id>/', views.delete_product, name='delete_product'),
    path("edit-product/<int:id>/", views.edit_product, name="edit_product"),
    path("product/<int:id>/", views.product_detail, name="product_detail"),
    path("search/", views.search, name="search"),

]
 

