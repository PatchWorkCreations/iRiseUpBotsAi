from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
from django.urls import path
import myapp.guest_views as guest_views

urlpatterns = [
    path('personalized_plan', views.personalized_plan, name='personalized_plan'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),

    path('about/', views.about, name='about'),
    path('blog-classic/', views.blogclassic, name='blogclassic'),
    path('blog/', views.blog, name='blog'),
    
    path('faq/', views.faq, name='faq'),

    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('like/<int:post_id>/', views.blog_like_post, name='blog_like_post'),
    path('dislike/<int:post_id>/', views.blog_dislike_post, name='blog_dislike_post'),
    path('blogs/<int:post_id>/comment/', views.blog_add_comment, name='blog_add_comment'),
    path('blogs/category/<int:category_id>/', views.blog_category, name='blog_category'),
    path('blogs/search/', views.blog_search, name='blog_search'),
    path('email-collection/', views.email_collection, name='email_collection'),
    path('iriseupdashboard/', views.iriseupdashboard, name='iriseupdashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('course/continue/<int:course_id>/', views.course_continue, name='course_continue'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('quiz-results/', views.quiz_results, name='quiz_results'),
    path('no-quiz-results/', views.no_quiz_results, name='no_quiz_results'),

    
    
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),

    path('support-center/', views.support_center, name='support_center'),
    path('knowledge-base/', views.knowledge_base, name='knowledge_base'),
    path('subcategory/<int:id>/', views.subcategory_detail, name='subcategory_detail'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),

    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment/', views.payment_page, name='payment_page'),
    path('success/', views.success_page, name='success_page'),

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('change-password/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-reset/invalid/', views.password_reset_invalid_link, name='password_reset_invalid_link'),

    path('submit-request/', views.submit_request, name='submit_request'),
    path('submit-request/success/', views.submit_request_success, name='submit_request_success'),

    # Forum
    path('forum/', views.forum_home, name='forum_home'),
    path('forum/category/<int:category_id>/', views.forum_category, name='forum_category'),
    path('forum/post/<int:post_id>/', views.forum_post_detail, name='forum_post_detail'),
    path('forum/new-post/', views.create_forum_post, name='create_forum_post'),
    path('search/', views.search, name='search'),
    path('forum/post/<int:post_id>/reply/<int:comment_id>/', views.reply_to_comment, name='reply_to_comment'),

    path('forum/profile/', views.forum_profile_view, name='forum_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit-avatar/', views.edit_avatar, name='edit_avatar'),

    path('course/<int:course_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('course/<int:course_id>/toggle-save/', views.toggle_save, name='toggle_save'),

    # Heritage Quiz
    path('heritage/question-1/', views.heritage_question_1, name='heritage_question_1'),
    path('heritage/question-2/', views.heritage_question_2, name='heritage_question_2'),
    path('heritage/question-3/', views.heritage_question_3, name='heritage_question_3'),
    path('heritage/question-4/', views.heritage_question_4, name='heritage_question_4'),
    path('heritage/question-5/', views.heritage_question_5, name='heritage_question_5'),
    path('heritage/question-6/', views.heritage_question_6, name='heritage_question_6'),
    path('heritage/question-7/', views.heritage_question_7, name='heritage_question_7'),
    path('heritage/question-8/', views.heritage_question_8, name='heritage_question_8'),
    path('heritage/question-9/', views.heritage_question_9, name='heritage_question_9'),
    path('heritage/question-10/', views.heritage_question_10, name='heritage_question_10'),
    path('heritage/question-11/', views.heritage_question_11, name='heritage_question_11'),
    path('heritage/question-12/', views.heritage_question_12, name='heritage_question_12'),
    path('heritage/question-13/', views.heritage_question_13, name='heritage_question_13'),
    path('heritage/question-14/', views.heritage_question_14, name='heritage_question_14'),
    path('heritage/question-15/', views.heritage_question_15, name='heritage_question_15'),
    path('heritage/question-16/', views.heritage_question_16, name='heritage_question_16'),
    path('heritage/question-17/', views.heritage_question_17, name='heritage_question_17'),
    path('heritage/question-18/', views.heritage_question_18, name='heritage_question_18'),
    path('heritage/question-19/', views.heritage_question_19, name='heritage_question_19'),
    path('heritage/heritage-summary/', views.heritage_summary, name='heritage_summary'),
    path('heritage/question-20/', views.heritage_question_20, name='heritage_question_20'),
    path('heritage/heritage-results/', views.heritage_results, name='heritage_results'),

    path('chat/', views.chat_interface, name='chat_interface'),
    path('api/chat/', views.get_response, name='get_response'),

    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('index', views.index, name='index'),
    path('index2', views.index2, name='index2'),
    
    path('api/chat/inspire/', views.get_inspire_response, name='get_inspire_response'),  # Ezra
    path('api/chat/pulse/', views.get_pulse_response, name='get_pulse_response'),        # Caleb
    path('api/chat/soulspark/', views.get_soulspark_response, name='get_soulspark_response'),  # Harper

     

    # Additional API Endpoints for Renamed Bots
     
    path('api/chat/mindforge/', views.get_mindforge_response, name='get_mindforge_response'),  # Einstein
    
    

    # Echo and Maven Chat API Endpoints and Views
    path('api/chat/echo/', views.get_echo_response, name='get_echo_response'),        # Echo
    path('api/chat/pathfinder/', views.get_pathfinder_response, name='get_pathfinder_response'),  # Maven
  

 
    path('api/chat/fortify/', views.get_fortify_response, name='get_fortify_response'),  

    
    path('personal_info_update/', views.personal_info_update, name='personal_info_update'),
    path('cancel_subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('personal_information/', views.personal_information, name='personal_information'),
    path('security/', views.security, name='security'),
    path('marketing_preferences/', views.marketing_preferences, name='marketing_preferences'),
    path('notification_setting/', views.notification_setting, name='notification_setting'),
    path('faq/', views.faq, name='faq'),
    path('data_privacy/', views.data_privacy, name='data_privacy'),
    path('about_amigo/', views.about_amigo, name='about_amigo'),
    path('feedback/', views.feedback, name='feedback'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('contact-us/', views.contactus, name='contactus'),
    path('delete_deactivate/', views.delete_deactivate, name='delete_deactivate'),
    path('deactivate_account/', views.deactivate_account, name='deactivate_account'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('account_deleted/', views.account_deleted, name='account_deleted'),
    path('account_deactivated/', views.account_deactivated, name='account_deactivated'),

    path('account/subscription-terms/', views.subscription_terms_new, name='account_subscription_terms'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('data-privacy/', views.data_privacy, name='data_privacy'),
    
    path('manage-payment-methods/', views.manage_payment_methods, name='manage_payment_methods'),
    path('update-payment-method/', views.update_payment_method, name='update_payment_method'),

    path('set-selected-plan/', views.set_selected_plan, name='set_selected_plan'),
    path('change_plan/', views.change_plan, name='change_plan'),



    path('elevate/', views.ezra_view, name='ezra'),
    path('thrive/', views.rudy_view, name='rudy'),
    path('lumos/', views.aria_view, name='aria'),
    path('mentor-iq/', views.einstein_view, name='einstein'),
    path('Nexara/', views.kash_view, name='kash'),
    path('imagine/', views.echo_view, name='echo'),
    path('gideon/', views.gideon_view, name='gideon'),
    path('keystone/', views.keystone_view, name='keystone'),

    # Shortened URLs
    path('ty/e/', views.ezra_thank_you, name='thankyou-ezra-short'),
    path('ty/t/', views.rudy_thank_you, name='thankyou-rudy-short'),
    path('ty/l/', views.aria_thank_you, name='thankyou-aria-short'),
    path('ty/miq/', views.einstein_thank_you, name='thankyou-einstein-short'),
    path('ty/n/', views.kash_thank_you, name='thankyou-kash-short'),
    path('ty/im/', views.echo_thank_you, name='thankyou-echo-short'),
    path('ty/g/', views.gideon_thank_you, name='thankyou-gideon-short'),
    path('ty/ks/', views.keystone_thank_you, name='thankyou-keystone-short'),

    # Readable URLs
    path('thankyou/elevate/', views.ezra_thank_you, name='thankyou-ezra'),
    path('thankyou/thrive/', views.rudy_thank_you, name='thankyou-rudy'),
    path('thankyou/lumos/', views.aria_thank_you, name='thankyou-aria'),
    path('thankyou/mentor-iq/', views.einstein_thank_you, name='thankyou-einstein'),
    path('thankyou/Nexara/', views.kash_thank_you, name='thankyou-kash'),
    path('thankyou/iamgine/', views.echo_thank_you, name='thankyou-echo'),
    path('thankyou/gideon/', views.gideon_thank_you, name='thankyou-gideon'),
    path('thankyou/keystone/', views.keystone_thank_you, name='thankyou-keystone'),


    #path('chat/<str:product_id>/', views.dynamic_chat, name='dynamic_chat'),

    path('manual-account-activation/', views.manual_account_activation, name='manual_account_activation'),
    path('send-test-email/', views.test_email_view, name='send_test_email'),

    path('dashboard/elevate/', views.elevate_dashboard, name='elevate_dashboard'),
    path('dashboard/thrive/', views.thrive_dashboard, name='thrive_dashboard'),
    path('dashboard/lumos/', views.lumos_dashboard, name='lumos_dashboard'),
    path('dashboard/imagine/', views.imagine_dashboard, name='imagine_dashboard'),
    path('dashboard/gideon/', views.gideon_dashboard, name='gideon_dashboard'),
    path('dashboard/mentor-iq/', views.mentor_iq_dashboard, name='mentor_iq_dashboard'),
    path('dashboard/Nexara/', views.nexus_dashboard, name='nexus_dashboard'),
    path('dashboard/keystone/', views.keystone_dashboard, name='keystone_dashboard'),
    path('validate-user-input/', views.validate_user_input, name='validate_user_input'),

    path('iriseupai_landing', views.iriseupai_landing, name='iriseupai_landing'),
    path('', views.chat_iriseupai, name='chat_iriseupai'),
    path('chat-iriseupai', views.chat_iriseupai, name='chat_iriseupai'),
    
    path('api/chat/lumos/', views.get_soulspark_response, name='get_soulspark_response'),  # Lumos (was soulspark)
    path('api/chat/mentor-iq/', views.get_mindforge_response, name='get_mindforge_response'),  # Mentor IQ (was mindforge)
    path('api/chat/elevate/', views.get_inspire_response, name='get_inspire_response'),  # Elevate (was inspire)
    path('api/chat/thrive/', views.get_pulse_response, name='get_pulse_response'),  # Thrive (was pulse)
    path('api/chat/imagine/', views.get_echo_response, name='get_echo_response'),  # Imagine (was echo)
    path('api/chat/gideon/', views.get_pathfinder_response, name='get_pathfinder_response'),  # Gideon (same)
    path('api/chat/Nexara/', views.get_bridge_response, name='get_bridge_response'),  # Nexara (was bridge)
    path('api/chat/keystone/', views.get_fortify_response, name='get_fortify_response'),
    
    # ✅ Test Endpoint
    path('api/guest/chat/<str:bot_name>/', guest_views.guest_bot_response, name='guest_bot_response'),
    path('signup/', views.signup_view, name='signup'),
    path('process-ai-subscription/', views.process_ai_subscription, name='process_ai_subscription'),

    path("api/get-user-plan/", views.get_user_plan, name="get-user-plan"),
    path("upgrade-to-pro/", views.upgrade_to_pro, name="upgrade_to_pro"),

    path('chat/<str:bot_name>/', views.chat_view, name='chat_view'),

    path("terms/", views.terms_view, name="terms"),


    path("test/", views.test, name="test"),
    path('chat_home/', views.chat_home, name="chat_home"),
    path('chat/<str:ai_name>/', views.test_chat_view, name="chat_view"),

    path('api/guest/chat/<str:bot_name>/', guest_views.guest_bot_response, name='guest_chat'),

    
    path('api/generate-image/', guest_views.guest_bot_response, name='generate_image'),

]
