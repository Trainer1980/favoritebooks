from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('process/reg', views.registration),
    path('process/login', views.login),
    path('books', views.main),
    path('book/<int:id>/fav', views.fav),
    path('books/new', views.new),
    path('books/<int:id>', views.book),
    path('books/<int:id>/update', views.update),
    path('books/user', views.user),
    path('logout', views.logout),
]