from django.contrib import admin
from .models import (
    Course, SubCourse, Lesson, UserCourseAccess, UserSubCourseAccess, 
    EmailCollection, ForumCategory, ForumPost, ForumComment, 
    BlogPost, BlogComment, Category, Tag, AIBot
)

# ✅ Course Admins
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


# ✅ Email Collection Admin
class EmailCollectionAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'receive_offers', 'created_at']  # Updated field name

    def user_email(self, obj):
        return obj.user.email if obj.user else None
    user_email.short_description = 'Email'  # This will change the column header in the admin

admin.site.register(EmailCollection, EmailCollectionAdmin)


# ✅ Forum Category Admin
admin.site.register(ForumCategory)


# ✅ Blog Admin
class BlogCommentInline(admin.TabularInline):  # Inline for comments
    model = BlogComment
    extra = 1  

@admin.register(BlogPost)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'author', 'publish_date', 'read_time')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('publish_date', 'author')
    date_hierarchy = 'publish_date'
    ordering = ('-publish_date',)
    inlines = [BlogCommentInline]  

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


# ✅ Forum Post Admin
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


# ✅ AIBot Admin (Fixed)
from django.utils.html import format_html
from django.contrib import admin
from .models import AIBot

@admin.register(AIBot)
class AIBotAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'ai_type', 'is_active', 'is_public', 'is_favorite', 'owner', 'preview_image'
    )
    search_fields = ('name', 'specialty', 'description', 'bio')
    list_filter = ('is_active', 'is_public', 'ai_type')
    readonly_fields = ('preview_image', 'created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'ai_type', 'specialty', 'description', 'bio')
        }),
        ('Media & Visuals', {
            'fields': ('image', 'preview_image')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_public', 'is_favorite', 'owner', 'cloned_from')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" style="border-radius:8px;" />', obj.image.url)
        return "No image"
    preview_image.short_description = 'AI Image'
