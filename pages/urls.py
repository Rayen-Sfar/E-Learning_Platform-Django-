from django.urls import path
from pages import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('join2', views.join2, name='join2'),
    path('indexLogin', views.indexLogin, name='indexLogin'), 

    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('courses', views.courses, name='courses'),
      # Fixed duplicate
    path('watch_video/<int:video_id>/', views.watch_video, name='watch_video'),

    path('playlist', views.playlist, name='playlist'),
    path('teacher_profile', views.teacher_profile, name='teacher_profile'),
    path('teachers', views.teachers, name='teachers'),
    path('update', views.update, name='update'),
   # path('watch_video', views.watch_video, name='watch_video'),
    path('teacher_private_account', views.teacher_private_account, name='teacher_private_account'),  # Fixed typo
    path('navbar', views.navbar, name='navbar'),  # Fixed typo
    path('logout',views.logout, name='logout')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    from django.conf import settings
from django.conf.urls.static import static

