import asyncio

from .forms import AchievementForm
from .models import *
from django.contrib import messages

from django.http import FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import os
from asgiref.sync import async_to_sync,sync_to_async





@csrf_exempt
# def upload_achievement(request):
#     if request.method == 'POST':
#         form = AchievementForm(request.POST, request.FILES)
#         print(form)
#         if form.is_valid():
#             files = form.cleaned_data['achievement_files']
#             for f in files:
#                 model = Achievement()
#                 model.achievement_files = f
#                 model.news_name_for = form.cleaned_data['news_name_for']
#                 model.save()
#             return redirect('index')
#     else:
#         form = AchievementForm()
#     return render(request, 'upload.html', {'form': form})

# Check if the user is an admin (superuser)
def admin_required(user):
    return user.is_superuser


def sanitize_filename(file):
    filename, ext = os.path.splitext(file.name)
    sanitized_name = slugify(filename) + ext
    file.name = sanitized_name
    return file


from django.shortcuts import render, redirect
from django.http import Http404
from .forms import AchievementForm  # Adjust based on your actual import
from .models import News, Achievement
import datetime



ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
ALLOWED_VIDEO_EXTENSIONS = ['.mp4']


def upload_achievement(request):
    if not request.user.is_superuser:
        raise Http404("Page not found")
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the News instance first
            news = News.objects.create(
                news_name=form.cleaned_data['news_name'],
                news_description=form.cleaned_data['news_description'],
                news_date=form.cleaned_data['news_date'] or datetime.datetime.now()
            )

            # Save Achievement files associated with the News
            files = request.FILES.getlist('achievement_files')  # Get list of uploaded files
            for f in files:
                achievement = Achievement(
                    news_name_for_achv=news,
                    achievement_files=f
                )
                achievement.save()

            return redirect('index')
    else:
        form = AchievementForm()
    return render(request, 'upload.html', {'form': form})


@csrf_exempt
def serve_media(request, file_path):
    file_path = os.path.join(settings.MEDIA_ROOT, file_path)
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        return response
    else:
        return HttpResponse("Media not found!")


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_email(to_email, first_name):
    subject = "Muvaffaqiyatli ro'yxatdan o'tish"
    from_email = 'admin@parkentpolitexnikum.uz'
    to = to_email

    # Render the HTML content using a template
    html_content = render_to_string('welcome_email_template.html', {'first_name': first_name})

    # Create plain text by stripping the HTML content
    text_content = strip_tags(html_content)

    # Create the email message object
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])

    # Attach the HTML content as an alternative
    msg.attach_alternative(html_content, "text/html")

    # Send the email
    msg.send()


def index(request):
    pictures = Homepage.objects.all()
    about_part_1 = About_part_1.objects.all()
    about_part_1_desc = About_part_1_desc.objects.all()
    carousel = Carousel_picture.objects.all()
    courses = Course.objects.all()
    our_group_photo = Our_group.objects.all()
    teachers = Teacher.objects.all()
    latest_post = News.objects.order_by('-news_date').first()
    print(latest_post)

    post_av = Achievement.objects.filter(news_name_for_achv=latest_post)

    files_with_types = []
    for achievement in post_av:
        file_url = achievement.achievement_files.url
        # Determine the file type
        if file_url.endswith('.mp4'):
            file_type = 'video'
        elif file_url.endswith(('.jpg', '.jpeg', '.png')):
            file_type = 'image'
        else:
            file_type = 'unknown'  # Fallback in case of unsupported file type

        files_with_types.append({
            'file': file_url,
            'type': file_type
        })

    return render(request, "index.html",
                  {"pictures": pictures, "about_part_1": about_part_1, "about_part_1_desc": about_part_1_desc,
                   "carousel": carousel, "courses": courses, "our_group_photo": our_group_photo, "teachers": teachers,
                   'latest_post': latest_post, "files_with_types": files_with_types,
        "length": len(files_with_types)})

def about(request):
    courses = Course.objects.all()
    datas = About_page_1.objects.all()
    teachers = Teacher.objects.all()
    goals = About_page_2.objects.all()
    return render(request, "about.html", {"courses": courses, "datas": datas, "teachers": teachers, 'goals': goals})


def navbar_only(request):
    courses = Course.objects.all()
    footer = Footer.objects.get()
    return render(request, "navbar_only.html", {"courses": courses, "footer": footer})


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import csv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
file_path = os.path.join(BASE_DIR, "about/registered_users.csv")
file_exists = os.path.isfile(file_path)
def save_to_csv(data):
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(
                ["ID", "Username", "Ism", "Yosh", "Manzil", "Telefon", "Sinf", "Yo'nalish", "Ta'lim shakli"])

        row = [
            data.get('user_id',"Noma'lum"),
            data.get('username',"Noma'lum"),
            data['first_name'],
            data['last_name'],
            data['place'],
            data['phone_number'],
            data['sinf'],
            data['major'],
            data.get('shape',"Noma'lum")
        ]
        writer.writerow(row)

class SubmitFormView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_number = request.data.get('phone_number')
        address=request.data.get('place')
        clas=request.data.get('sinf')
        major=request.data.get('major')
        shape=request.data.get('shape',"Noma'lum")
        email = request.data.get('email')



        if Register.objects.filter(gmail=email).exists():
            message = "Bu google akkauntdan allaqachon ro'yxatdan o'tilgan yoki siz allaqachon ro'yxatdan o'tkansiz!"
        else:
            user = Register(first_name=first_name, last_name=last_name, phone_number=phone_number, address=address,clas=clas,major=major,shape=shape,gmail=email)
            user.save()

            send_welcome_email(email, first_name)
            if clas == "9":
                notification_message = (
                    f"<strong>Yangi foydalanuvchi sayt orqali ro'yxatdan o'tdi👀</strong>\n\n"
                    f"Ism🕵️: <strong>{first_name}</strong>\n"
                    f"Familiya💁‍♂️: <strong>{last_name}</strong>\n"
                    f"Telefon raqam📲: <strong>{phone_number}</strong>\n"
                    f"Gmail📧: <strong>{email}</strong>\n"
                    f"Address📍: <strong>{address}</strong>\n"
                    f"Sinf🔢: <strong>{clas}</strong>\n"
                    f"Yo'nalish📚: <strong>{major}</strong>"
                )
                save_to_csv(request.data)
                send_telegram_message(notification_message)

            else:
                notification_message = (
                    f"<strong>Yangi foydalanuvchi sayt orqali ro'yxatdan o'tdi👀</strong>\n\n"
                    f"Ism🕵️: <strong>{first_name}</strong>\n"
                    f"Familiya💁‍♂️: <strong>{last_name}</strong>\n"
                    f"Telefon raqam📲: <strong>{phone_number}</strong>\n"
                    f"Gmail📧: <strong>{email}</strong>\n"
                    f"Address📍: <strong>{address}</strong>\n"
                    f"Sinf🔢: <strong>{clas}</strong>\n"  # <strong> ni yopib qo'ydim
                    f"Yo'nalish📚: <strong>{major}</strong>\n"
                    f"Ta'lim shakli🔖: <strong>{shape}</strong>"
                )
                save_to_csv(request.data)
                send_telegram_message(notification_message)

            message = f"Muvaffaqiyatli ro'yxatdan o'tildi! Iltimos {email} nomli pochtangizni tekshiring biz unga xabar yubordik🧑‍💻"

        return Response({"message": message}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        return Response({"message": "Invalid request method."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


import requests

from .env import BOT_TOKEN,ADMINS




def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Check if CHAT_IDS is a list
    if isinstance(ADMINS, list):
        for chat_id in ADMINS:
            payload = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': "HTML"
            }
            requests.post(url, data=payload)


def courses(request):
    courses = Course.objects.all()
    return render(request, "courses.html", {"courses": courses})


def every_course(request, pk):
    courses = Course.objects.all()
    video=Footer.objects.all()
    course_pk = get_object_or_404(Course, pk=pk)
    onecourse = EveryCourse.objects.filter(course_name  =course_pk)
    skills = EveryCourseSkills.objects.filter(course_name_for_skill=course_pk)
    teachers = Teacher.objects.filter(teacher_major=course_pk)
    carousel = Carousel_picture.objects.all()
    return render(request, "every_course.html",
                  {"courses": courses, "onecourse": onecourse, "skills": skills, "teachers": teachers,
                   "carousel": carousel,"video":video})



def news(request):
    news_posts = News.objects.order_by('-news_date')
    courses=Course.objects.all()
    # For each news post, get all related achievements and determine the file type
    news_with_achievements = []
    for news_item in news_posts:
        achievements_with_type = []
        for achievement in news_item.achievements.all():
            file_url = achievement.achievement_files.url
            # Determine if the file is an image or a video
            if file_url.endswith('.mp4'):
                file_type = 'video'
            elif file_url.endswith(('.jpg', '.jpeg', '.png')):
                file_type = 'image'
            else:
                file_type = 'unknown'  # Fallback for unsupported file types

            achievements_with_type.append({
                'achievement': achievement,
                'file_type': file_type,
                'file_url': file_url,
            })

        news_with_achievements.append({
            'news_item': news_item,
            'achievements': achievements_with_type,
        })

    context = {
        'news_with_achievements': news_with_achievements,
        'courses':courses,
    }

    return render(request, "news.html", context)


def edit_news(request, news_id):
    if not request.user.is_superuser:
        raise Http404("Page not found")
    news_instance = get_object_or_404(News, id=news_id)

    # Check if the POST request contains updated data
    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES, instance=news_instance)

        if form.is_valid():
            # Save changes to the News object and associated achievements
            form.save()
            return redirect('index')  # Redirect to the news detail page after saving

    else:
        # Pre-fill the form with the existing news data
        form = AchievementForm(instance=news_instance)

    return render(request, 'edit_news.html', {'form': form, 'news': news_instance})
from django.contrib.auth import authenticate, login,logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('index')  # Redirect to a 'home' or other desired page after login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("index")
    
    
def delete_post(request,post_id=None):
    if not request.user.is_superuser:
        raise Http404("Page not found")
    post_to_delete=News.objects.get(id=post_id)
    print(post_to_delete)
    post_to_delete.delete()
    return redirect("index") 
    
def news_detail(request,slug):
    courses = Course.objects.all()
    news_one = get_object_or_404(NewsSlug, slug=slug)
    news_item = get_object_or_404(News, pk=news_one.news.pk)
    post_av = Achievement.objects.filter(news_name_for_achv=news_item)

    files_with_types = []
    for achievement in post_av:
        file_url = achievement.achievement_files.url
        # Determine the file type
        if file_url.endswith('.mp4'):
            file_type = 'video'
        elif file_url.endswith(('.jpg', '.jpeg', '.png')):
            file_type = 'image'
        else:
            file_type = 'unknown'

        files_with_types.append({
            'file': file_url,
            'type': file_type
        })
    return render(request, 'news_detail.html', {
        'news_item': news_item,
        'files_with_types': files_with_types,
        'courses':courses,
        'news_slug':news_one.slug
    })    


from rest_framework import generics
from  .serializers import CourseSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]
    http_method_names = ['get']




class CourseRetrieveView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated | HasAPIKey]
    http_method_names = ['get']