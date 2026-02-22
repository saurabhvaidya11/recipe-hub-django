from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from vege import views
from vege.views import (
    receipes, delete_receipe, update_receipe,
    login_page, register_page, logout_page
)

urlpatterns = [
    path('', receipes, name="home"),
    path('receipes/', receipes, name="receipes"),
    path('delete-receipe/<int:id>/', delete_receipe, name="delete_receipe"),
    path('update-receipe/<int:id>/', update_receipe, name="update_receipe"),

    path('admin/', admin.site.urls),

    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('logout/', logout_page, name="logout_page"),

    # Password reset
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html'
         ),
         name='password_reset'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('like/<int:id>/', views.like_receipe, name="like_receipe"),
    path('comment/<int:id>/', views.add_comment, name="add_comment"),
    path('delete-comment/<int:id>/', views.delete_comment, name="delete_comment"),
    path('receipe/<int:pk>/', views.receipe_detail, name="receipe_detail"),
    path('add-receipe/', views.add_receipe, name="add_receipe"),

    path('profile/settings/', views.profileSetting, name='profileSetting'),
    path('profile/update/', views.profile_update, name="profile_update"),
    path('profile/delete/', views.profile_delete, name="profile_delete"),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
]

# MEDIA FILES SERVING
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)