from django.urls import path, include
from myapp import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index2, name='index2'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),

    path('index', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog-classic/', views.blogclassic, name='blogclassic'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('index-3/', views.index3, name='index3'),

    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('like/<int:post_id>/', views.blog_like_post, name='blog_like_post'),
    path('dislike/<int:post_id>/', views.blog_dislike_post, name='blog_dislike_post'),
    path('blogs/<int:post_id>/comment/', views.blog_add_comment, name='blog_add_comment'),
    path('blogs/category/<int:category_id>/', views.blog_category, name='blog_category'),
    path('blogs/search/', views.blog_search, name='blog_search'),


    path('not-found/', views.notfound, name='notfound'),
    path('pricing/', views.pricing, name='pricing'),
    path('register/', views.register, name='register'),
    path('reset/', views.reset, name='reset'),
    path('service-detail/', views.servicedetail, name='servicedetail'),
    path('services/', views.services, name='services'),
    path('team-detail/', views.teamdetail, name='teamdetail'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('news-detail1/', views.newsdetail1, name='newsdetail1'),
    path('news-detail2/', views.newsdetail2, name='newsdetail2'),
    path('news-detail3/', views.newsdetail3, name='newsdetail3'),
    path('news-detail4/', views.newsdetail4, name='newsdetail4'),
    path('news-detail5/', views.newsdetail5, name='newsdetail5'),
    path('news-detail6/', views.newsdetail6, name='newsdetail6'),
    path('news-detail7/', views.newsdetail7, name='newsdetail7'),
    path('news-detail8/', views.newsdetail8, name='newsdetail8'),
    path('service-detail1/', views.servicedetail1, name='servicedetail1'),
    path('service-detail2/', views.servicedetail2, name='servicedetail2'),
    path('service-detail3/', views.servicedetail3, name='servicedetail3'),
    path('service-detail4/', views.servicedetail4, name='servicedetail4'),
    path('service-detail5/', views.servicedetail5, name='servicedetail5'),
    path('coursemenu/', views.coursemenu, name='coursemenu'),

    path('quiz/', views.combined_quiz, name='combined_quiz'),
    path('sub_courses/<int:sub_course_id>/', views.sub_course_detail, name='sub_course_detail'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    
    path('lessons/<int:lesson_id>/next/', views.next_lesson, name='next_lesson'),
    path('lessons/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),

    path('course/continue/<int:course_id>/', views.course_continue, name='course_continue'),

    path('start_quiz/', views.start_quiz, name='start_quiz'),
    path('age_selection/', views.age_selection, name='age_selection'),

    path('after-age/', views.after_age_page, name='after_age_page'),

    path('main_goal/', views.main_goal, name='main_goal'),
    path('income_source/', views.income_source, name='income_source'),
    path('work_schedule/', views.work_schedule, name='work_schedule'),
    path('job_challenges/', views.job_challenges, name='job_challenges'),

    path('after-job-challenges/', views.after_job_challenges_page, name='after_job_challenges_page'),
    
    path('financial_situation/', views.financial_situation, name='financial_situation'),

    path('comfortable-financial/', views.comfortable_financial, name='comfortable_financial'),
    path('stability-financial/', views.stability_financial, name='stability_financial'),
    path('struggling-financial/', views.struggling_financial, name='struggling_financial'),
    
    path('annual-income-goal/', views.annual_income_goal, name='annual_income_goal'),
    path('control-work-hours/', views.control_work_hours, name='control_work_hours'),
    path('routine-work/', views.routine_work, name='routine_work'),
    path('time-saved-use/', views.time_saved_use, name='time_saved_use'),


    
    path('job_interest_match/', views.job_interest_match, name='job_interest_match'),

    path('absolutely-interest/', views.absolutely_interest, name='absolutely_interest'),
    path('somewhat-interest/', views.somewhat_interest, name='somewhat_interest'),
    path('maybe-interest/', views.maybe_interest, name='maybe_interest'),
    path('not-necessarily-interest/', views.not_necessarily_interest, name='not_necessarily_interest'),
    

    path('digital_business_knowledge/', views.digital_business_knowledge, name='digital_business_knowledge'),
    path('side_hustle_experience/', views.side_hustle_experience, name='side_hustle_experience'),
    path('learning_new_skills/', views.learning_new_skills, name='learning_new_skills'),
    path('ai_tools_familiarity/', views.ai_tools_familiarity, name='ai_tools_familiarity'),
    path('content_writing_knowledge/', views.content_writing_knowledge, name='content_writing_knowledge'),
    path('digital_marketing_knowledge/', views.digital_marketing_knowledge, name='digital_marketing_knowledge'),
    path('ai_income_boost_awareness/', views.ai_income_boost_awareness, name='ai_income_boost_awareness'),
    path('fields_interest/', views.fields_interest, name='fields_interest'),
    path('ai_mastery_readiness/', views.ai_mastery_readiness, name='ai_mastery_readiness'),

    path('all-set/', views.all_set, name='all_set'),
    path('ready/', views.ready, name='ready'),
    path('somewhat-ready/', views.somewhat_ready, name='somewhat_ready'),
    path('not-ready/', views.not_ready, name='not_ready'),
    
    path('focus_ability/', views.focus_ability, name='focus_ability'),
    path('special_goal/', views.special_goal, name='special_goal'),
    path('time_to_achieve_goal/', views.time_to_achieve_goal, name='time_to_achieve_goal'),
    path('summary/', views.summary, name='summary'),
    path('results/', views.results, name='results'),
    # Other paths...
    path('loading/', views.loading_page, name='loading_page'),
    path('email-collection/', views.email_collection, name='email_collection'),
    path('readiness-level/', views.readiness_level, name='readiness_level'),
   
    path('subscription-terms/', views.subscription_terms, name='subscription_terms'),
    path('terms-conditions/', views.terms_conditions, name='terms_conditions'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),  # Privacy Policy URL

    path('support-center/', views.support_center, name='support_center'),  # Support Center URL
    path('knowledge-base/', views.knowledge_base, name='knowledge_base'),
    path('subcategory/<int:id>/', views.subcategory_detail, name='subcategory_detail'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('personalized-plan/', views.personalized_plan, name='personalized_plan'),
    path('process-payment/', views.process_payment, name='process_payment'),
     # URL pattern for the payment page
    path('payment/', views.payment_page, name='payment_page'),

    # Success page after successful payment
    path('success/', views.success_page, name='success_page'),
    path('preview-email/', views.preview_email, name='preview_email'),

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #path('change-password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('change-password/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('change-password/done/', views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-reset/invalid/', views.password_reset_invalid_link, name='password_reset_invalid_link'),
    

    #path('create-paypal-order/', views.create_paypal_order, name='create_paypal_order'),
    path('create-paypal-product/', views.create_paypal_product_view, name='create_paypal_product'),
    path('create-paypal-plan/', views.create_paypal_subscription_plan_view, name='create_paypal_plan'),
    path('complete-paypal-subscription/', views.complete_paypal_subscription, name='complete_paypal_subscription'),
    path('set-selected-plan/', views.set_selected_plan, name='set_selected_plan'),
    path('get-paypal-plan-id/', views.get_paypal_plan_id, name='get-paypal-plan-id'),
    path('paypal/webhook/', views.paypal_webhook, name='paypal_webhook'),


    path('profile/', views.profile_view, name='profile'),
    # path('update-profile/', views.update_profile, name='update_profile'),
    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('quiz-results/', views.quiz_results, name='quiz_results'),
    path('no-quiz-results/', views.no_quiz_results, name='no_quiz_results'),

    path('submit-request/', views.submit_request, name='submit_request'),
    path('submit-request/success/', views.submit_request_success, name='submit_request_success'),

    #forum
    path('forum/', views.forum_home, name='forum_home'),

    # Forum Category - Lists all posts in a category
    path('forum/category/<int:category_id>/', views.forum_category, name='forum_category'),

    # Forum Post Detail - View a single post and its comments
    path('forum/post/<int:post_id>/', views.forum_post_detail, name='forum_post_detail'),

    # Create Forum Post - Form to create a new post
    path('forum/new-post/', views.create_forum_post, name='create_forum_post'),
    path('search/', views.search, name='search'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('forum/post/<int:post_id>/reply/<int:comment_id>/', views.reply_to_comment, name='reply_to_comment'),


    path('forum/profile/', views.forum_profile_view, name='forum_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit-avatar/', views.edit_avatar, name='edit_avatar'),

    path('course/<int:course_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('course/<int:course_id>/toggle-save/', views.toggle_save, name='toggle_save'),

    path('heritage/', views.heritage_page, name='heritage_page'),
    path('heritage/main-goal/', views.heritage_main_goal, name='heritage_main_goal'),
   
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
    path('heritage/question-21/', views.heritage_question_21, name='heritage_question_21'),

    path('chat/', views.chat_interface, name='chat_interface'),
    path('api/chat/', views.get_response, name='get_response'),

    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]
