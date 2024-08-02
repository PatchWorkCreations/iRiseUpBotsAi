from django.contrib import admin
from .models import Course, Lesson, UserCourseAccess

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'units', 'hours')
    search_fields = ('title',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')

class UserCourseAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'progress')
    list_filter = ('course', 'user')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(UserCourseAccess, UserCourseAccessAdmin)
