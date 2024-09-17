from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/', views.create_listing, name='create_listing'),
    path('listing/<slug:slug>/', views.listing_detail, name='listing_detail'),
    path('listing/<int:listing_id>/bid/', views.create_bid, name='create_bid'),
    path('listing/<int:listing_id>/comment/', views.create_comment, name='create_comment'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('listing/<int:listing_id>/finish/', views.finish_auction, name='finish_auction'),
    path('listing/<int:listing_id>/watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    path('watchlist/list/',views.wathclist,name='wathclist'),
    path('prueba', views.prueba, name="prueba")
   
]
