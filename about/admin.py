from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Homepage)

admin.site.register(About_part_1)
admin.site.register(About_part_1_desc)
admin.site.register(Carousel_picture)
admin.site.register(Our_group)
admin.site.register(About_page_1)
admin.site.register(Register)
admin.site.register(About_page_2)
admin.site.register(EveryCourse)
admin.site.register(EveryCourseSkills)
admin.site.register(Footer)
admin.site.register(Achievement)

@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ["news_name","pk"]

@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    search_fields = ["course_name"]

@admin.register(Teacher)
class AdminTeacher(admin.ModelAdmin):
    list_display = ["teacher_fullname","teacher_major"]
    search_fields = ["teacher_fullname"]
