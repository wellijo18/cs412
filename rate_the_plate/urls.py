# rate_the_plate/urls.py

from django.urls import path
from .views import CarListView, CarDetailView, CreateCarView, ReviewDetailView, CreateReviewView, DeleteReviewView, UpdateReviewView, AddReactionView, RemoveReactionView, CreateCommentView, MyAccountView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path('', CarListView.as_view(), name='show_all_cars'),
    path('account/', MyAccountView.as_view(), name='my_account'),
    path('car/<int:pk>', CarDetailView.as_view(), name='car'),
    path('review/<int:pk>', ReviewDetailView.as_view(), name='review'),
    path('car/<int:pk>/create_review', CreateReviewView.as_view(), name='create_review'),
    path('review/<int:pk>/delete', DeleteReviewView.as_view(), name='delete_review'),
    path('review/<int:pk>/update', UpdateReviewView.as_view(), name='update_review'),
    path('review/<int:pk>/like', AddReactionView.as_view(), name='like_review'),
    path('review/<int:pk>/dislike', AddReactionView.as_view(), name='dislike_review'),
    path('review/<int:pk>/remove_reaction', RemoveReactionView.as_view(), name='remove_reaction'),
    path('review/<int:pk>/comment', CreateCommentView.as_view(), name='create_comment'),
    path('login/', auth_views.LoginView.as_view(template_name='rate_the_plate/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logout_confirmation/', TemplateView.as_view(template_name='rate_the_plate/logged_out.html'), name='logout_confirmation'),
    path('car/create', CreateCarView.as_view(), name='create_car'),
]