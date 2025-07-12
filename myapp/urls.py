from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
from django.urls import path
import myapp.guest_views as guest_views
from myapp import views

urlpatterns = [
    path('personalized_plan', views.personalized_plan, name='personalized_plan'),
    path('sign_in/', views.sign_in_regular, name='sign_in'),

    path('sign_out/', views.sign_out, name='sign_out'),


    path('iriseupdashboard/', views.chat_iriseupai_sandbox, name='iriseupdashboard'),

    
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


    path('chat/', views.chat_interface, name='chat_interface'),
    path('api/chat/', views.get_response, name='get_response'),

    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
 
    
    path('api/chat/inspire/', views.get_elevate_response, name='get_elevate_response'),  # Ezra
    path('api/chat/pulse/', views.get_thrive_response, name='get_thrive_response'),        # Caleb
    path('api/chat/soulspark/', views.get_lumos_response, name='get_lumos_response'),  # Harper

     

    # Additional API Endpoints for Renamed Bots
     
    path('api/chat/mindforge/', views.get_mentor_iq_response, name='get_mentor_iq_response'),  # Einstein
    
    

    # Echo and Maven Chat API Endpoints and Views
    path('api/chat/echo/', views.get_imagine_response, name='get_imagine_response'),        # Echo
    path('api/chat/pathfinder/', views.get_gideon_response, name='get_gideon_response'),  # Maven
  

 
    path('api/chat/fortify/', views.get_keystone_response, name='get_keystone_response'),  

    
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
    
    path('api/chat/lumos/', views.get_lumos_response, name='get_lumos_response'),  # Lumos (was soulspark)
    path('api/chat/mentor-iq/', views.get_mentor_iq_response, name='get_mentor_iq_response'),  # Mentor IQ (was mindforge)
    path('api/chat/elevate/', views.get_elevate_response, name='get_elevate_response'),  # Elevate (was inspire)
    path('api/chat/thrive/', views.get_thrive_response, name='get_thrive_response'),  # Thrive (was pulse)
    path('api/chat/imagine/', views.get_imagine_response, name='get_imagine_response'),  # Imagine (was echo)
    path('api/chat/gideon/', views.get_gideon_response, name='get_gideon_response'),  # Gideon (same)
    path('api/chat/Nexara/', views.get_nexara_response, name='get_nexara_response'),  # Nexara (was bridge)
    path('api/chat/keystone/', views.get_keystone_response, name='get_keystone_response'),
    path('api/chat/nexara/', views.get_nexara_response, name='get_nexara_response'),  # Nexara (was bridge)

    # ✅ Test Endpoint
    path('api/guest/chat/<str:bot_name>/', guest_views.guest_bot_response, name='guest_bot_response'),
    path('signup/', views.signup_view, name='signup'),
    path('process-ai-subscription/', views.process_ai_subscription, name='process_ai_subscription'),

    path("api/get-user-plan/", views.get_user_plan, name="get-user-plan"),
    path("upgrade-to-pro/", views.upgrade_to_pro, name="upgrade_to_pro"),

    path("api/guest/count/", guest_views.get_guest_count, name="get_guest_count"),

    path("terms/", views.terms_view, name="terms"),


    path("test/", views.test, name="test"),
    path('chat_home/', views.chat_home, name="chat_home"),
    

    path('api/guest/chat/<str:bot_name>/', guest_views.guest_bot_response, name='guest_chat'),

    
    path('api/generate-image/', guest_views.guest_bot_response, name='generate_image'),
    path('sandbox_ai/', views.chat_home, name="chat_home"),


    path("api/chat-history/", views.get_chat_history, name="chat-history-list"),


    path("api/chat-history/<int:chat_id>/", views.get_chat_history, name="chat-history-detail"),

    path("api/chat/send-message/", views.send_message, name="send_message"),


    #######################################################################################

   

    # ✅ Get All Chat History (Right Sidebar)
    path("api/get_chat_history/", views.get_chat_history, name="get_chat_history"),

    # ✅ Get Specific Chat by ID (Clicking on a chat)
    path('api/get_chat/<int:chat_id>/', views.get_chat, name='get_chat'),

    # ✅ Send Message to AI (Middle Chat Box)
    path("api/chat/stream_message/", views.simple_chat_message, name="stream_chat_message"),

    path("api/chat/message/", views.simple_chat_message, name="simple_chat_message"),

    # ✅ Rename Chat Title (Manual User Edit)
    path("api/chat/<int:chat_id>/rename/", views.rename_chat_title, name="rename_chat_title"),

    # ✅ Reset Chat Title (Re-enable AI Naming)
    path("api/chat/<int:chat_id>/reset_title/", views.reset_chat_title, name="reset_chat_title"),

    path("sandbox/", views.iriseupdashboard, name="chat_iriseupai_sandbox"),
    path("looks/", views.look, name="look"),

    path("api/create_ai_bot/", views.create_ai_bot, name="create_ai_bot"),
    path("api/toggle_favorite/<int:bot_id>/", views.toggle_favorite_ai_bot, name="toggle_favorite_ai_bot"),
    path("api/delete_ai_bot/<int:bot_id>/", views.delete_ai_bot, name="delete_ai_bot"),
    path("api/ai_list/", views.get_ai_bots, name="get_ai_bots"),
    path('api/update_ai_bot/<int:bot_id>/', views.update_ai_bot, name='update_ai_bot'),
    path("set-language/", views.set_language, name="set_language"),
    path('zoho-domain-verification.html', views.zoho_verification, name='zoho_verify'),




    path('converter/', views.html_to_django_view, name='html_to_django'),
    path('generate-views/', views.generate_views_py, name='generate_views'),
    path('generate-urls/', views.generate_urls_py, name='generate_urls'),

    path('iriseup/', views.landing_for_iriseup, name='landing_for_iriseup'),
    path('about-us/', views.about_us, name='about_us'),
    path('service/', views.service, name='service'),
    path('connect-with-us/', views.iriseup_contact_us, name='iriseup_contact_us'),
    path("api/save_reminder/", views.save_reminder, name="save_reminder"),

    path('iriseup/investor/', views.investor_page, name='investor_page'),

    path('iriseup/services/', views.services, name='services'),
    
    path('ai-integration/', views.ai_integration, name='ai_integration'),

    path("ai-integration/calendar/", views.calendar, name="ai_integration_calendar"),
    path("ai-integration/charts-apex/", views.charts_apex, name="ai_integration_charts_apex"),
    path("ai-integration/charts-chartjs/", views.charts_chartjs, name="ai_integration_charts_chartjs"),
    path("ai-integration/components-accordions/", views.components_accordions, name="ai_integration_components_accordions"),
    path("ai-integration/components-block-ui/", views.components_block_ui, name="ai_integration_components_block_ui"),
    path("ai-integration/components-cards/", views.components_cards, name="ai_integration_components_cards"),
    path("ai-integration/components-carousel/", views.components_carousel, name="ai_integration_components_carousel"),
    path("ai-integration/components-countdown/", views.components_countdown, name="ai_integration_components_countdown"),
    path("ai-integration/components-lightbox/", views.components_lightbox, name="ai_integration_components_lightbox"),
    path("ai-integration/components-lists/", views.components_lists, name="ai_integration_components_lists"),
    path("ai-integration/components-modals/", views.components_modals, name="ai_integration_components_modals"),
    path("ai-integration/components-session-timeout/", views.components_session_timeout, name="ai_integration_components_session_timeout"),
    path("ai-integration/components-tabs/", views.components_tabs, name="ai_integration_components_tabs"),
    path("ai-integration/content-boxed-content/", views.content_boxed_content, name="ai_integration_content_boxed_content"),
    path("ai-integration/content-left-menu/", views.content_left_menu, name="ai_integration_content_left_menu"),
    path("ai-integration/content-page-headings/", views.content_page_headings, name="ai_integration_content_page_headings"),
    path("ai-integration/content-right-menu/", views.content_right_menu, name="ai_integration_content_right_menu"),
    path("ai-integration/content-section-headings/", views.content_section_headings, name="ai_integration_content_section_headings"),
    path("ai-integration/error/", views.error, name="ai_integration_error"),
    path("ai-integration/file-manager/", views.file_manager, name="ai_integration_file_manager"),
    path("ai-integration/forms-basic/", views.forms_basic, name="ai_integration_forms_basic"),
    path("ai-integration/forms-datepickers/", views.forms_datepickers, name="ai_integration_forms_datepickers"),
    path("ai-integration/forms-file-upload/", views.forms_file_upload, name="ai_integration_forms_file_upload"),
    path("ai-integration/forms-input-groups/", views.forms_input_groups, name="ai_integration_forms_input_groups"),
    path("ai-integration/forms-input-masks/", views.forms_input_masks, name="ai_integration_forms_input_masks"),
    path("ai-integration/forms-layouts/", views.forms_layouts, name="ai_integration_forms_layouts"),
    path("ai-integration/forms-select2/", views.forms_select2, name="ai_integration_forms_select2"),
    path("ai-integration/forms-text-editor/", views.forms_text_editor, name="ai_integration_forms_text_editor"),
    path("ai-integration/forms-validation/", views.forms_validation, name="ai_integration_forms_validation"),
    path("ai-integration/header-basic/", views.header_basic, name="ai_integration_header_basic"),
    path("ai-integration/header-colorful/", views.header_colorful, name="ai_integration_header_colorful"),
    path("ai-integration/header-full-width/", views.header_full_width, name="ai_integration_header_full_width"),
    path("ai-integration/header-large/", views.header_large, name="ai_integration_header_large"),
    path("ai-integration/header-transparent/", views.header_transparent, name="ai_integration_header_transparent"),
    path("ai-integration/index/", views.index, name="ai_integration_index"),
    path("ai-integration/invoice/", views.invoice, name="ai_integration_invoice"),
    path("ai-integration/lock-screen/", views.lock_screen, name="ai_integration_lock_screen"),
    path("ai-integration/mailbox/", views.mailbox, name="ai_integration_mailbox"),
    path("ai-integration/menu-colored-sidebar/", views.menu_colored_sidebar, name="ai_integration_menu_colored_sidebar"),
    path("ai-integration/menu-dark-sidebar/", views.menu_dark_sidebar, name="ai_integration_menu_dark_sidebar"),
    path("ai-integration/menu-hover-menu/", views.menu_hover_menu, name="ai_integration_menu_hover_menu"),
    path("ai-integration/menu-off-canvas/", views.menu_off_canvas, name="ai_integration_menu_off_canvas"),
    path("ai-integration/menu-standard/", views.menu_standard, name="ai_integration_menu_standard"),
    path("ai-integration/pricing/", views.pricing, name="ai_integration_pricing"),
    path("ai-integration/create_bot/", views.create_bot, name="ai_integration_create_bot"),
    path("ai-integration/sign-in/", views.sign_in, name="ai_integration_sign_in"),
    path("ai-integration/sign-up/", views.sign_up, name="ai_integration_sign_up"),
    path("ai-integration/styles-code/", views.styles_code, name="ai_integration_styles_code"),
    path("ai-integration/styles-icons/", views.styles_icons, name="ai_integration_styles_icons"),
    path("ai-integration/styles-typography/", views.styles_typography, name="ai_integration_styles_typography"),
    path("ai-integration/tables-basic/", views.tables_basic, name="ai_integration_tables_basic"),
    path("ai-integration/tables-datatable/", views.tables_datatable, name="ai_integration_tables_datatable"),
    path("ai-integration/todo/", views.todo, name="ai_integration_todo"),
    path("ai-integration/ui-alerts/", views.ui_alerts, name="ai_integration_ui_alerts"),
    path("ai-integration/ui-avatars/", views.ui_avatars, name="ai_integration_ui_avatars"),
    path("ai-integration/ui-badge/", views.ui_badge, name="ai_integration_ui_badge"),
    path("ai-integration/ui-breadcrumbs/", views.ui_breadcrumbs, name="ai_integration_ui_breadcrumbs"),
    path("ai-integration/ui-button-groups/", views.ui_button_groups, name="ai_integration_ui_button_groups"),
    path("ai-integration/ui-buttons/", views.ui_buttons, name="ai_integration_ui_buttons"),
    path("ai-integration/ui-collapse/", views.ui_collapse, name="ai_integration_ui_collapse"),
    path("ai-integration/ui-dropdown/", views.ui_dropdown, name="ai_integration_ui_dropdown"),
    path("ai-integration/ui-images/", views.ui_images, name="ai_integration_ui_images"),
    path("ai-integration/ui-pagination/", views.ui_pagination, name="ai_integration_ui_pagination"),
    path("ai-integration/ui-popovers/", views.ui_popovers, name="ai_integration_ui_popovers"),
    path("ai-integration/ui-progress/", views.ui_progress, name="ai_integration_ui_progress"),
    path("ai-integration/ui-spinners/", views.ui_spinners, name="ai_integration_ui_spinners"),
    path("ai-integration/ui-toast/", views.ui_toast, name="ai_integration_ui_toast"),
    path("ai-integration/ui-tooltips/", views.ui_tooltips, name="ai_integration_ui_tooltips"),
    path("ai-integration/widgets/", views.widgets, name="ai_integration_widgets"),
    path("ai-integration/dashboard/", views.ai_integration_dashboard, name="ai_integration_dashboard"),
    path("ai-integration/sign-up/", views.ai_register, name="ai_integration_sign_up"),
    path('dashboard/', views.dashboard_view, name='ai_integration_dashboard'),
    path('sign-up/', views.ai_register, name='ai_integration_sign_up'),
    path('ai-sign-in/', views.ai_sign_in, name='ai_integration_sign_in'),
    path('bots/delete/<int:bot_id>/', views.delete_ai_bot, name='ai_integration_delete_bot'),


    path('signup-quiz/', views.signup_quiz, name='signup_quiz'),
    path('submit-answer/', views.submit_quiz_answer, name='submit_quiz_answer'),

    path("staff-attendance/", views.staff_attendance, name="staff_attendance"),
    path("iriseup-login/", views.login_view, name="iriseup_login"),

    path('qr_generator/', views.qr_generator, name='qr_generator'),
    path('qr-dashboard/', views.qr_list, name='qr_list'),

    path('scan/<int:pk>/', views.scan_redirect, name='scan_redirect'),

    path('qr/update/', views.update_qr, name='update_qr'),
    path('qr/delete/', views.delete_qr, name='delete_qr'),

]


