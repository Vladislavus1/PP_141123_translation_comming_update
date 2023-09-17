from django.urls import path
from .views import render_main_page, render_article_form_page, \
    render_all_articles_page, render_single_article,\
    render_profile_page, render_add_preferences_page, \
    send_comment, edit_description, reaction, search,\
    render_remove_preferences_page, render_add_preferences_page, \
    edit_profile_photo, subscribe, render_about_us_page, \
    write_a_review, send_comment_2, comment

urlpatterns = [
    path("", render_main_page, name="render_main_page"),
    path("create_article", render_article_form_page, name="render_article_form_page"),
    path("all_articles", render_all_articles_page, name="render_all_articles_page"),
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
    path("comment/<int:comment_id>", comment, name="comment")
]
