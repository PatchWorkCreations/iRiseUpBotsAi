from django.contrib import admin
from .models import Course, SubCourse, Lesson, UserCourseAccess, UserSubCourseAccess

class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_course', 'parent_sub_course')
    search_fields = ('title', 'parent_sub_course__title', 'parent_sub_course__parent_course__title')

    def get_course(self, obj):
        return obj.parent_sub_course.parent_course.title
    get_course.short_description = 'Course'

class SubCourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_course', 'units', 'hours')
    search_fields = ('title', 'parent_course__title')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'units', 'hours')
    search_fields = ('title',)

admin.site.register(Course, CourseAdmin)
admin.site.register(SubCourse, SubCourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(UserCourseAccess)
admin.site.register(UserSubCourseAccess)


from django.contrib import admin
from .models import EmailCollection

class EmailCollectionAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'receive_offers', 'created_at']  # Updated field name

    def user_email(self, obj):
        return obj.user.email if obj.user else None
    user_email.short_description = 'Email'  # This will change the column header in the admin

admin.site.register(EmailCollection, EmailCollectionAdmin)


from django.contrib import admin
from .models import ForumCategory

# Register the ForumCategory model
admin.site.register(ForumCategory)

# Registering the Blog model in the admin
from django.contrib import admin
from .models import BlogPost  # Import your BlogPost model

@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # Automatically generate the slug from the title
    list_display = ('title', 'author', 'publish_date', 'read_time')
    search_fields = ('title', 'content', 'author')  # Allows searching by title, content, and author
    list_filter = ('publish_date', 'author')  # Filters for author and publish date
    date_hierarchy = 'publish_date'  # Adds a date-based drilldown navigation
    ordering = ('-publish_date',)  # Orders by publish date descending


