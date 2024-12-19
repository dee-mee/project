from django.urls import path
from .views import homepage, recipe_detail, profile, contact, landing_page, history
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', landing_page, name='landing_page'),  # Landing Page
    path('homepage/', homepage, name='homepage'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('profile/', profile, name='profile'),
    path('history/', profile, name='history'),  # Example: Reuse profile view for history
    path('contact/', contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='recipes/login.html'), name='login'),  # Login URL
    path('signup/', views.signup, name='signup'),  # Signup URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
]

