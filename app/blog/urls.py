from django.urls import path
from .views import render_main_page, render_article_form_page, \
    render_single_article,\
    render_profile_page, render_add_preferences_page, \
    send_comment, edit_description, reaction, search,\
    render_remove_preferences_page, render_add_preferences_page, \
    edit_profile_photo, subscribe, render_about_us_page, \
    write_a_review, send_comment_2, comment, render_subscriptions_page, \
    comment_reaction, comment_reaction2, delete_article, edit_comment, \
    delete_comment, edit_comment2, delete_comment2, user_notifications, \
    close_notification, render_filtered_page, render_leaderboard_page

urlpatterns = [
    path("", render_main_page, name="render_main_page"),
    path("create_article", render_article_form_page, name="render_article_form_page"),
    # path("all_articles", render_all_articles_page, name="render_all_articles_page"),
    path("article/<int:article_id>", render_single_article, name="render_single_article"),
    path("profile/<int:user_id>", render_profile_page, name="render_profile_page"),
    path("send_comment/<int:article_id>", send_comment, name="send_comment"),
    path("edit_description/<int:user_id>", edit_description, name="edit_description"),
    path("article/<str:action>/<int:article_id>", reaction, name="reaction"),
    path("profile/article/<str:action>/<int:article_id>", reaction, name="reaction"),
    path("search", search, name="search"),
    path("settings/preferences/add", render_add_preferences_page, name="render_add_preferences_page"),
    path("settings/preferences/remove", render_remove_preferences_page, name="render_remove_preferences_page"),
    path("settings/preferences", render_add_preferences_page, name="render_add_preferences_page"),
    path("edit_profile_photo", edit_profile_photo, name="edit_profile_photo"),
    path("subscribe/<int:user_id>", subscribe, name="subscribe"),
    path("settings/about_us", render_about_us_page, name="render_about_us_page"),
    path("settings/write_a_review", write_a_review, name="write_a_review"),
    path("send_comment_2/<int:comment_id>", send_comment_2, name="send_comment_2"),
    path("comment/<int:comment_id>", comment, name="comment"),
    path("subscriptions", render_subscriptions_page, name="render_subscriptions_page"),
    path("comment/<str:action>/<int:comment_id>", comment_reaction, name="comment_reaction"),
    path("comment2/<str:action>/<int:comment_id>", comment_reaction2, name="comment_reaction2"),
    path('delete_article/<int:article_id>', delete_article, name="delete_article"),
    path('edit_comment/<int:comment_id>', edit_comment, name="edit_comment"),
    path('delete_comment/<int:comment_id>', delete_comment, name='delete_comment'),
    path('comment2_edit_comment/<int:comment2_id>', edit_comment2, name='edit_comment2'),
    path('comment2_delete_comment/<int:comment2_id>', delete_comment2, name='delete_comment2'),
    path('notifications', user_notifications, name='user_notifications'),
    path('close_notification/<str:notif_type>/<int:notification_id>', close_notification, name='close_notification'),
    path('filter', render_filtered_page, name='render_filtered_page'),
    path('leaderboard', render_leaderboard_page, name='render_leaderboard_page')
]
