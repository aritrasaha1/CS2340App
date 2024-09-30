# restaurants/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.http import Http404

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('map/', views.map_view, name='map'),  # Restaurant search
    # path('profile/', views.profile, name='profile'),  # Removed profile URL
    
    # Login and logout with error handling in case of invalid login attempts
    path('accounts/login/', 
         auth_views.LoginView.as_view(template_name='registration/login.html'), 
         name='login'),
    
    path('accounts/logout/', 
         auth_views.LogoutView.as_view(), 
         name='logout'),  # Logout

    # Signup page with a check for invalid forms
    path('accounts/signup/', views.signup, name='signup'),  # Corrected name

    # Favorites page with validation to ensure user is authenticated
    path('favorites/', views.favorites, name='favorites'),

    # Add to favorite with validation on restaurant ID format
    path('add_favorite/', views.add_favorite, name='add_favorite'),  # Add favorite

    # Remove from favorites with error handling for invalid or non-existent restaurant IDs
    path('remove_favorite/<str:place_id>/', 
         views.remove_favorite, 
         name='remove_favorite'),

    # Restaurant details view with a check for invalid place_id or missing data
    path('restaurant/<str:place_id>/', 
         views.restaurant_detail, 
         name='restaurant_detail'),

    # Password reset flow with added security and proper feedback to the user
    path('accounts/password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), 
         name='password_reset'),

    path('accounts/password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),

    path('accounts/reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),

    path('accounts/reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),
]

# Error handling added in the views
def handle_not_found(request, exception):
    raise Http404("The requested page could not be found.")
