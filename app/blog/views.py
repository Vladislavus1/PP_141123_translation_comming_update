from django.shortcuts import render, redirect
# from .forms import ArticleForm
from django.http import JsonResponse
from .controllers import *
import re
# Create your views here.


def render_main_page(request):
    if request.user.is_authenticated:
        all_articles = get_all_articles()
        user_preferences = request.user.preferences
        new_articles = get_articles_published_last_hour()
        articles_you_like = []

        def custom_sort_key(item):
            if re.match(r'^\d+$', item):  # Проверяем, является ли строка числом
                return (1, int(item))  # Сортировка чисел на первом месте
            else:
                return (0, item)

        sorted_user_preferences_list = sorted(user_preferences, key=custom_sort_key)

        for article in all_articles:
            sorted_preferences_list = sorted(article.tags, key=custom_sort_key)
            for item in sorted_user_preferences_list:
                if item in sorted_preferences_list:
                    articles_you_like.append(article)
                else:
                    pass
        print(new_articles)
        return render(request, 'all_articles.html',
                      context={"all_articles": all_articles, "articles_you_like": articles_you_like, "new_articles": new_articles})
    else:
        return render(request, "main.html", context={"user": request.user})

def render_article_form_page(request):
    if request.method == "POST":
        article_data = request.POST.dict()
        title = article_data["title"]
        content = article_data["content"]
        picture_url = article_data["picture_url"]
        tags = []
        for index in range(1, 12):
            tag = article_data[f"tag{index}"]
            print(tag)
            if tag == "" or tag == None:
                pass
            else:
                tags.append(tag)
        print(request.user)
        print(request.user.id)
        create_article_with_success_message(request, title, content, picture_url, request.user, tags)
        return redirect('/all_articles')
    username = str(request.user)
    print(username)
    return render(request, "create_article.html", context={"username": username, "user": request.user})

def render_all_articles_page(request):
    all_articles = get_all_articles()
    user_preferences = request.user.preferences
    new_articles = get_articles_published_last_hour()
    articles_you_like = []

    def custom_sort_key(item):
        if re.match(r'^\d+$', item):  # Проверяем, является ли строка числом
            return (1, int(item))  # Сортировка чисел на первом месте
        else:
            return (0, item)

    sorted_user_preferences_list = sorted(user_preferences, key=custom_sort_key)

    for article in all_articles:
        sorted_preferences_list = sorted(article.tags, key=custom_sort_key)
        for item in sorted_user_preferences_list:
            if item in sorted_preferences_list:
                articles_you_like.append(article)
            else:
                pass
    print(new_articles)
    return render(request, 'all_articles.html', context={"all_articles": all_articles, "articles_you_like": articles_you_like, "new_articles": new_articles})
    # articles_i_like = get_articles_i_like()
    # new_articles = get_all_new_articles

def render_single_article(request, article_id):
    article = get_article_by_id(article_id)
    likes = len(article.likes)
    dislikes = len(article.dislikes)
    comments = get_comments_for_article(article_id)
    return render(request, "single_article.html", context={"article": article, "comments": comments, 'likes': likes, "dislikes": dislikes, "get_other_comments": get_other_comments})

def render_profile_page(request, user_id):
    print(request.user.id)
    user = get_user_by_id(user_id)
    articles = get_all_articles_for_user(user.id)
    subscribers = len(user.subscribers)
    subscriptions = len(user.subscriptions)
    if user_id == request.user.id:
        account_permission = "Account_permission"
        return render(request, "profile.html",
                      context={"user_info": user, "subscribers": subscribers, "subscriptions": subscriptions,
                               "articles": articles, "account_permission": account_permission})
    else:
        if request.user.id in user.subscribers and user.id in request.user.subscriptions:
            already_subscribed = "already_subscribed"
            return render(request, "profile.html",
                          context={"user_info": user, "subscribers": subscribers, "subscriptions": subscriptions,
                                   "articles": articles, "already_subscribed": already_subscribed})
        else:
            return render(request, "profile.html",
                          context={"user_info": user, "subscribers": subscribers, "subscriptions": subscriptions,
                                   "articles": articles})
def render_add_preferences_page(request):
    all_preferences = get_all_preferences()
    user_preferences = request.user.preferences
    new_user_preferences = []
    preferences = []
    for item in user_preferences:
        preference = get_tag_by_name(item)
        new_user_preferences.append(preference)
    for item in all_preferences:
        if item in new_user_preferences:
            pass
        else:
            preferences.append(item)
    if request.method == "POST":
        form_data = request.POST.dict()
        form_list = list(form_data.items())
        form_list.pop(0)
        form_data = dict(form_list)
        print(form_data)
        list_of_id = []
        for key in form_data:
            new_str_id = key[:0] + key[10:]
            new_id = int(new_str_id)
            list_of_id.append(new_id)
        for int_id in list_of_id:
            tag = get_tag_by_id(int_id)
            request.user.preferences.append(tag)
            request.user.save()
        # for i in range(1, len(preferences)):
        #     try:
        #         preference = form_data[f"preference{i}"]
        #         print(form_data[f"preference{i}"])
        #         request.user.add_preferences(preference)
        #         request.user.save()
        #     except:
        #         pass
        print(form_data)
        return redirect("/all_articles")
    return render(request, "preferences_add.html", context={"preferences": preferences})

def render_remove_preferences_page(request):
    user_preferences = request.user.preferences
    preferences = []
    print(preferences)
    for item in user_preferences:
        preference = get_tag_by_name(item)
        preferences.append(preference)
    print(preferences)
    if request.method == "POST":
        form_data = request.POST.dict()
        form_list = list(form_data.items())
        form_list.pop(0)
        form_data = dict(form_list)
        print(form_data)
        list_of_id = []
        for key in form_data:
            new_str_id = key[:0] + key[10:]
            new_id = int(new_str_id)
            list_of_id.append(new_id)
        for int_id in list_of_id:
            tag = get_tag_by_id(int_id)
            request.user.preferences.remove(tag.name_of_topic)
            request.user.save()
        # form_data = request.POST.dict()
        # for i in range(1, len(preferences)):
        #     try:
        #         preference = form_data[f"preference{i}"]
        #         print(form_data[f"preference{i}"])
        #         request.user.remove_preferences(preference)
        #         request.user.save()
        #     except:
        #         pass
        print(form_data)
        return redirect("/all_articles")
    return render(request, "preferences_remove.html", context={"preferences": preferences})

def render_about_us_page(request):
    return render(request, "about_us_page.html")

def write_a_review(request):
    if request.method == "POST":
        form_data = request.POST.dict()
        review_content = form_data["review_content"]
        number_of_stars = form_data["rating"]
        create_review(request, review_content, number_of_stars)
        return redirect("/all_articles")
    return render(request, "review_page.html")

def send_comment(request, article_id):
    if request.method == "POST":
        user = get_user_by_id(request.user.pk)
        comment_data = request.POST.dict()
        content = comment_data["content"]
        create_comment_for_article(user, content, article_id)
        return redirect(f"/article/{article_id}")

def send_comment_2(request, comment_id):
    if request.method == "POST":
        form_data = request.POST.dict()
        user = request.user
        content = form_data["comment2Data"]
        comment = get_comment_by_id(comment_id)
        create_answer_for_comment(user, content, comment_id)
        return redirect(f"/article/{comment.article.id}")

def comment(request, comment_id):
    print(comment_id)
    comments_2 = get_other_comments(comment_id)
    json_dict = {'comments': {}}
    for comment in comments_2:
        author = str(comment.author.username)
        content = comment.content
        published_date = str(format_datetime(comment.published_date))
        profile_profile = comment.author.profile_picture
        comment_dict = {'author': author, 'profile_picture': profile_profile, 'content': content, 'published_date': published_date}
        json_dict['comments'][f'comment{comment.id}'] = comment_dict
    print(json_dict)
    return JsonResponse(json_dict)

        # published_date = str(comment.published_date)

def edit_description(request, user_id):
    if request.method == "POST":
        form_data = request.POST.dict()
        new_description = form_data["new_description"]
        user = request.user
        edit_description_for_user(user, new_description)
        return redirect(f"/profile/{user_id}")

def edit_profile_photo(request):
    if request.method == "POST":
        form_data = request.POST.dict()
        profile_photo = form_data["new_profile_photo_url"]
        user = request.user
        edit_pfp_for_user(user, profile_photo)
        return redirect(f"/profile/{user.id}")

def subscribe(request, user_id):
    if request.method == "POST":
        user2 = get_user_by_id(user_id)
        to_subscribe(request, user2)
        return redirect(f"/profile/{user_id}")

def reaction(request, action, article_id):
    record = Articles.objects.get(pk=article_id)
    try:
        if action == 'like':
            record.to_like(request.user.id)
            print(request.user.id, "-- тут")
        elif action == 'dislike':
            record.to_dislike(request.user.id)
    except Exception as e:
        print(e)
        resp_data = str(e)
    return redirect(f'/article/{article_id}')

def search(request):
    search_query = request.GET.get('query')
    articles = get_all_articles_by_search_query(search_query)
    return render(request, 'article_by_search_query.html', context={'articles': articles, "search_query": search_query})

