# import os
# import django
# from django.shortcuts import get_object_or_404
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
# django.setup()
#
# from about.models import *
#
# latest_post = News.objects.order_by('-news_date')
#
# for news_item in latest_post:
#     # Get all achievements related to the current news item
#     achievements = news_item.achievements.all()
#
#     print(f"News: {news_item.news_name} (ID: {news_item.pk})")
#
#     # Loop through each achievement of this news item
#     for achievement in achievements:
#         print(f"Achievement file: {achievement.achievement_files} for News ID: {news_item.pk}")

# print(f.footer)
# course_name =
# course_name = EveryCourse.objects.filter(course_name=course_name.course_name)

# # for i in Homepage.objects.all():
# #     print(i.home_picture)
# # p=Homepage.objects.all()
# # for i in p:
# #     print(i.home_picture)
#
# p=Teacher.objects.all()
# for i in p:
#     print(i.teacher_major)

# import http.client
#
# conn = http.client.HTTPSConnection("apilayer.net")
#
# # Headers including your NumVerify API key
# headers = {
#     'access_key': 'YOUR_ACCESS_KEY_HERE'
# }
#
# # Example phone number and country code
# phone_number = "+59894887799"
#
# # Send the GET request
# conn.request("GET", f"/api/validate?access_key=YOUR_ACCESS_KEY_HERE&number={phone_number}")
#
# # Get the response
# res = conn.getresponse()
# data = res.read()
#
# # Print the response data
# print(data.decode("utf-8"))
#
# # Close the connection
# conn.close()
import os

file_path = os.path.join(os.getcwd(), "Admins.txt")  # This will load the file from the current working directory
print(f"Looking for file at: {file_path}")
