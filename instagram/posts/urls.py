from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homeSite'),
    path('post/', views.create_post, name='postSite'),
    path('signup/', views.signup, name='signupSite'),
    path('login/', views.login_view, name='loginSite'),
    path('logout/', views.logout_view, name='logoutSite'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('profile/<str:username>/', views.profile, name='profileSite'),
]