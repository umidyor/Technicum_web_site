from django.urls import path
from .views import upload_achievement,serve_media,about,index,SubmitFormView,courses,every_course,news,edit_news,logout_view,login_view,delete_post,news_detail,CourseListView,CourseRetrieveView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
urlpatterns = [
    path('upload/', upload_achievement, name='upload_achievement'),
    path('media/<path:file_path>',serve_media,name='serve_media'),
    path('about',about,name='about'),
    path('',index,name='index'),
    path('api/submit-form/', SubmitFormView.as_view(), name='submit_form'),
    path('courses',courses,name='courses'),
    path('courses/<int:pk>',every_course,name="every_course"),
    path('news',news,name="news"),
    path('news/<int:news_id>/edit/', edit_news, name='edit_news'),
    path('login',login_view,name='login'),
    path('logout',logout_view,name='logout'),
    path("delete/<int:post_id>/",delete_post,name='delete'),
    path("news/<str:slug>",news_detail,name='news_detail'),

    path('api/courses/', CourseListView.as_view(), name='api_courses_list'),
    path("api/courses/<pk>", CourseRetrieveView.as_view(), name="api_courses_id")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)