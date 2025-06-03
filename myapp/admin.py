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



from django.contrib import admin
from .models import (
    AIIntegrationAccount,
    TeamMember,
    AddOn,
    UserAddOn,
    UserIntegrationBot,
    TrainingSession,
    Document,
    AnalyticsSnapshot,
    AIIntegrationSubscriptionPlan
)

@admin.register(AIIntegrationSubscriptionPlan)
class AIIntegrationSubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_monthly', 'bot_limit', 'doc_page_limit', 'api_request_limit', 'is_active')
    list_filter = ('code', 'is_active')
    search_fields = ('name', 'description')


@admin.register(AIIntegrationAccount)
class AIIntegrationAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'bots_created', 'documents_uploaded', 'api_requests_today', 'is_active')
    list_filter = ('plan__code', 'expiration_date')
    search_fields = ('user__username',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('email', 'owner', 'role', 'accepted', 'invited_on')
    list_filter = ('accepted', 'role')
    search_fields = ('email', 'owner__username')


@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price')
    search_fields = ('name', 'code')


@admin.register(UserAddOn)
class UserAddOnAdmin(admin.ModelAdmin):
    list_display = ('user', 'addon', 'quantity', 'activated_on')
    search_fields = ('user__username', 'addon__name')


@admin.register(UserIntegrationBot)
class UserIntegrationBotAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'template', 'created_at')
    search_fields = ('name', 'user__username')
    list_filter = ('created_at',)


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('bot', 'created_at')
    search_fields = ('bot__name', 'bot__user__username')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'bot', 'page_count', 'last_embedded')
    search_fields = ('name', 'user__username', 'bot__name')


@admin.register(AnalyticsSnapshot)
class AnalyticsSnapshotAdmin(admin.ModelAdmin):
    list_display = ('user', 'bot', 'date', 'total_chats', 'total_users')
    list_filter = ('date',)
    search_fields = ('user__username', 'bot__name')


from .models import QuizQuestion, QuizChoice, UserQuizAnswer

class QuizChoiceInline(admin.TabularInline):
    model = QuizChoice
    extra = 2

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'order']
    ordering = ['order']
    inlines = [QuizChoiceInline]
    search_fields = ['question_text']

@admin.register(UserQuizAnswer)
class UserQuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'selected_choice', 'answered_at']
    search_fields = ['user__username', 'question__question_text', 'selected_choice__choice_text']
    list_filter = ['answered_at']
