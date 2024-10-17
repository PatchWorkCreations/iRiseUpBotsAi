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

from django.contrib import admin
from .models import BlogPost, BlogComment, Category, Tag  # Import the models

# Define the inline for comments
class BlogCommentInline(admin.TabularInline):  # or use admin.StackedInline for a different layout
    model = BlogComment
    extra = 1  # How many empty comment forms to display by default

# Register the BlogPost model with the inline comments
@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'author', 'publish_date', 'read_time')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('publish_date', 'author')
    date_hierarchy = 'publish_date'
    ordering = ('-publish_date',)
    inlines = [BlogCommentInline]  # This will add the inline for comments

# Register Category and Tag models to make them available in admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


from django.contrib import admin
from .models import ForumPost, ForumComment

# Admin for Forum-related models
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('category', 'created_at', 'updated_at')
    actions = ['delete_selected_posts']

    def delete_selected_posts(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Selected posts have been deleted.")
    delete_selected_posts.short_description = "Delete selected forum posts"

class ForumCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content', 'author__username')

admin.site.register(ForumPost, ForumPostAdmin)
admin.site.register(ForumComment, ForumCommentAdmin)
