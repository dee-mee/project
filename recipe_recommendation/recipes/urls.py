from django.urls import path
from .views import homepage, recipe_detail, profile, contact_view, landing_page, history_view, all_recipes, download_recipe, \
    history_view
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', landing_page, name='landing_page'),  # Landing Page
    path('homepage/', homepage, name='homepage'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('all-recipes/', all_recipes, name='all_recipes'),
    path('profile/', profile, name='profile'),
    path('history/', history_view, name='history'),
    path('recipe/<int:recipe_id>/download/', download_recipe, name='download_recipe'),
    path('contact/', contact_view, name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='recipes/login.html'), name='login'),  # Login URL
    path('signup/', views.signup, name='signup'),  # Signup URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
]

