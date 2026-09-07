from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from bsd_operating_systems import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bsd-os/', views.homepage_view, name='homepage'),
    path('', views.homepage_view, name='root'),
    # Authentication URLs:
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    # Comment URLs:
    path('bsd-os/comment/delete/<int:os_id>/', views.delete_comment_view, name='delete_comment'),
    # OS Management URLs (only superuser):
    path('bsd-os/create/', views.create_os_view, name='create_os'),
    path('bsd-os/edit/<int:pk>/', views.edit_os_view, name='edit_os'),
    path('bsd-os/delete/<int:pk>/', views.delete_os_view, name='delete_os'),
]

# Add media file serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)