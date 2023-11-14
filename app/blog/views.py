from django.shortcuts import render, redirect
# from .forms import ArticleForm
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.http import JsonResponse
from .controllers import *
import re
from .lists_for_work import list_of_bad_words
import requests
# Create your views here.


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        return File(img_temp)

    return None

def render_main_page(request):
    if request.user.is_authenticated:
        get_numeral_of_notifications_for_user(request.user)
        all_articles = get_all_articles()
        return render(request, 'all_articles.html',
                      context={"all_articles": all_articles})
    else:
        return render(request, "main.html", context={"user": request.user})

# def render_main_page(request):
#     if request.user.is_authenticated:
#         get_numeral_of_notifications_for_user(request.user)
#         all_articles = get_all_articles()
#         user_preferences = request.user.preferences
#         new_articles = get_articles_published_last_hour()
#         articles_you_like = []
#         def custom_sort_key(item):
#             if re.match(r'^\d+$', item):  # Проверяем, является ли строка числом
#                 return (1, int(item))  # Сортировка чисел на первом месте
#             else:
#                 return (0, item)
#
#         sorted_user_preferences_list = sorted(user_preferences, key=custom_sort_key)
#
#         for article in all_articles:
#             sorted_preferences_list = sorted(article.tags, key=custom_sort_key)
#             for item in sorted_user_preferences_list:
#                 if item in sorted_preferences_list:
#                     if article in articles_you_like:
#                         pass
#                     else:
#                         articles_you_like.append(article)
#                 else:
#                     pass
#         print(articles_you_like, "тут")
#         return render(request, 'all_articles.html',
#                       context={"all_articles": all_articles, "articles_you_like": articles_you_like, "new_articles": new_articles})
#     else:
#         return render(request, "main.html", context={"user": request.user})

# def render_article_form_page(request):
#     if request.method == "POST":
#         article_data = request.POST.dict()
#         title = article_data["title"]
#         content = article_data["content"]
#         picture_url = article_data["picture_url"]
#         tags = []
#         for index in range(1, 12):
#             tag = article_data[f"tag{index}"]
#             print(tag)
#             if tag == "" or tag == None:
#                 pass
#             else:
#                 tags.append(tag)
#         print(request.user)
#         print(request.user.id)
#         create_article_with_success_message(request, title, content, picture_url, request.user, tags)
#         return redirect('/all_articles')
#     username = str(request.user)
#     print(username)
#     return render(request, "create_article.html", context={"username": username, "user": request.user})

def contains_prohibited_words(text):
    prohibited_words = list_of_bad_words  # Замените на свои запрещенные слова
    normalized_text = text.lower()
    for word in prohibited_words:
        if word in normalized_text:
            return True

    return False


def render_article_form_page(request):
    get_numeral_of_notifications_for_user(request.user)
    if request.method == "POST":
        article_data = request.POST.dict()
        title = article_data["title"]
        content = article_data["content"]
        tags = []
        # Добавляем проверку на содержание запрещенных слов в контенте
        if contains_prohibited_words(content) or contains_prohibited_words(title):
            messages.warning(request, 'Your article contains profanity that is not allowed on our platform.\nPlease be polite!')
            return redirect('/create_article')

        picture_url = article_data["picture_url"]
        for index in range(1, 12):
            tag = article_data[f"tag{index}"]
            print(tag)
            if tag == "" or tag == None:
                pass
            else:
                tags.append(tag)
        tags = [tag for tag in tags if not contains_prohibited_words(tag)]
        create_article_with_success_message(request, title, content, picture_url, request.user, tags)
        return redirect('/')

    username = str(request.user)
    return render(request, "create_article.html", context={"username": username, "user": request.user})

def render_subscriptions_page(request):
    get_numeral_of_notifications_for_user(request.user)
    list_of_subscriptions = request.user.subscriptions
    print(list_of_subscriptions)
    all_articles = get_articles_from_subscriptions(list_of_subscriptions)
    return render(request, 'subscriptions_page.html', context={'all_articles': all_articles})

# def render_all_articles_page(request):
#     get_numeral_of_notifications_for_user(request.user)
#     all_articles = get_all_articles()
#     user_preferences = request.user.preferences
#     new_articles = get_articles_published_last_hour()
#     articles_you_like = []
#     print(type(request.user.notifications), type(request.user.notifications), request.user.notifications)
#     def custom_sort_key(item):
#         if re.match(r'^\d+$', item):  # Проверяем, является ли строка числом
#             return (1, int(item))  # Сортировка чисел на первом месте
#         else:
#             return (0, item)
#
#     sorted_user_preferences_list = sorted(user_preferences, key=custom_sort_key)
#
#     for article in all_articles:
#         sorted_preferences_list = sorted(article.tags, key=custom_sort_key)
#         for item in sorted_user_preferences_list:
#             if item in sorted_preferences_list:
#                 if article in articles_you_like:
#                     pass
#                 else:
#                     articles_you_like.append(article)
#             else:
#                 pass
#     print(articles_you_like)
#     return render(request, 'all_articles.html', context={"all_articles": all_articles, "articles_you_like": articles_you_like, "new_articles": new_articles})
### turned on --> "on"
### turned off --> not transferable --> KeyError
def render_filtered_page(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        try:
            if form_data['inlineRadioOptions'] == 'best':
                best_articles = get_best_articles()
                needed_articles = []
                if form_data['rankValue'] == 'all':
                    needed_articles = best_articles
                else:
                    for article in best_articles:
                        needed_amount = form_data['rankValue']
                        result = check_article_likes_amount(article, needed_amount)
                        match result:
                            case True:
                                needed_articles.append(article)
                            case False:
                                pass
            elif form_data['inlineRadioOptions'] == 'new':
                new_articles = get_articles_published_last_hour()
                needed_articles = []
                if form_data['rankValue'] == 'all':
                    needed_articles = new_articles
                else:
                    for article in new_articles:
                        needed_amount = form_data['rankValue']
                        result = check_article_likes_amount(article, needed_amount)
                        match result:
                            case True:
                                needed_articles.append(article)
                            case False:
                                pass
        except KeyError:
            new_articles = get_articles_published_last_hour()
            needed_articles = []
            if form_data['rankValue'] == 'all':
                needed_articles = new_articles
            else:
                for article in new_articles:
                    needed_amount = form_data['rankValue']
                    result = check_article_likes_amount(article, needed_amount)
                    match result:
                        case True:
                            needed_articles.append(article)
                        case False:
                            pass
    import random
    filtered_articles = list(needed_articles)
    random.shuffle(filtered_articles)
    print(filtered_articles)
    return render(request, 'filtered_articles_page.html', context={'filtered_articles': filtered_articles})

def render_single_article(request, article_id):
    get_numeral_of_notifications_for_user(request.user)
    article = get_article_by_id(article_id)
    likes = len(article.likes)
    dislikes = len(article.dislikes)
    comments = get_comments_for_article(article_id)
    return render(request, "single_article.html", context={"article": article, "comments": comments, 'likes': likes, "dislikes": dislikes, "get_other_comments": get_other_comments})

def render_leaderboard_page(request):
    best_authors = get_best_authors()
    return render(request, 'leaderboard_page.html', context={'best_authors': best_authors})

def render_profile_page(request, user_id):
    get_numeral_of_notifications_for_user(request.user)
    print(request.user.id)
    user = get_user_by_id(user_id)
    articles = get_all_articles_for_user(user.id)
    subscribers = len(user.subscribers)
    subscriptions = len(user.subscriptions)
    status = check_user_status(user_id)
    if user_id == request.user.id:
        account_permission = "Account_permission"
        return render(request, "profile.html",
                      context={"user_info": user, "subscribers": subscribers, "subscriptions": subscriptions,
                               "articles": articles, "account_permission": account_permission, 'status': status})
    else:
        if request.user.id in user.subscribers and user.id in request.user.subscriptions:
            already_subscribed = "already_subscribed"
            return render(request, "profile.html",
                          context={"user_info": user, "subscribers": subscribers, "subscriptions": subscriptions,
                                   "articles": articles, "already_subscribed": already_subscribed, 'status': status})
        else:
            return render(request, "profile.html",
                          context={"user_info": user, "subscribers": subscribers, "subscriptions": subscriptions,
                                   "articles": articles, 'status': status})

def render_add_preferences_page(request):
    get_numeral_of_notifications_for_user(request.user)
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
        return redirect("/")
    return render(request, "preferences_add.html", context={"preferences": preferences})

def render_remove_preferences_page(request):
    get_numeral_of_notifications_for_user(request.user)
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
        return redirect("/")
    return render(request, "preferences_remove.html", context={"preferences": preferences})

def render_about_us_page(request):
    get_numeral_of_notifications_for_user(request.user)
    return render(request, "about_us_page.html")

def write_a_review(request):
    get_numeral_of_notifications_for_user(request.user)
    if request.method == "POST":
        form_data = request.POST.dict()
        review_content = form_data["review_content"]
        number_of_stars = form_data["rating"]
        create_review(request, review_content, number_of_stars)
        return redirect("/")
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

def user_notifications(request):
    get_numeral_of_notifications_for_user(request.user)
    reaction_notifications = get_reaction_notifications(request.user.id)
    comment_layer1_notifications = get_comment_layer1_notifications(request.user.id)
    comment_layer2_notifications = get_comment_layer2_notifications(request.user.id)
    return render(request, 'user_notifications.html', context={'reaction_notifications': reaction_notifications, 'comment_layer1_notifications': comment_layer1_notifications, 'comment_layer2_notifications': comment_layer2_notifications})

def close_notification(request, notif_type, notification_id):
    match notif_type:
        case 'com1':
            delete_notification(Comment_layer1_Notification, notification_id)
            return redirect('/notifications')
        case 'com2':
            delete_notification(Comment_layer2_Notification, notification_id)
            return redirect('/notifications')
        case 'reaction':
            delete_notification(Reaction_Notification, notification_id)
            return redirect('/notifications')

def comment(request, comment_id):
    print(comment_id)
    comments_2 = get_other_comments(comment_id)
    json_dict = {'comments': {}}
    for comment in comments_2:
        comment_id = comment.id
        author = str(comment.author.username)
        author_id = comment.author.id
        content = comment.content
        published_date = str(format_datetime(comment.published_date))
        profile_profile = comment.author.profile_picture
        likes = comment.get_likes()
        dislikes = comment.get_dislikes()
        status = comment.status
        comment_dict = {'author': author,
                        'profile_picture': profile_profile,
                        'content': content,
                        'published_date': published_date,
                        'comment_id': comment_id,
                        'likes': likes,
                        'dislikes': dislikes,
                        'authorId': author_id,
                        'requestUserId': request.user.id,
                        'status': status}
        json_dict['comments'][f'comment{comment.id}'] = comment_dict
    print(json_dict)
    return JsonResponse(json_dict)

def edit_comment2(request, comment2_id):
    comment2 = get_comment2_by_id(comment2_id)
    print(comment2)
    if request.method == 'POST':
        comment2_data = request.POST.dict()
        print(comment2.content)
        edited_comment_data = comment2_data['comment2EditData']
        comment2.content = edited_comment_data
        print(comment2.content)
        comment2.status = 'edited'
        comment2.publish()
        return redirect(f"/article/{comment2.comment.article.id}")
        # published_date = str(comment.published_date)

def edit_comment(request, comment_id):
    if request.method == "POST":
        form_data = request.POST.dict()
        comment = get_comment_by_id(comment_id)
        comment.content = form_data["commentEditData"]
        comment.status = 'edited'
        comment.publish()
        return redirect(f'/article/{comment.article.id}')

def delete_comment(request, comment_id):
    comment = get_comment_by_id(comment_id)
    if request.user.id == comment.author.id:
        pass
    else:
        messages.warning(request, 'You have no permission to delete this comment!')
        return redirect('/')
    if request.method == 'POST':
        comment.delete()
        return redirect(f'/article/{comment.article.id}')

def delete_comment2(request, comment2_id):
    print('hiiiiiiii')
    comment2 = get_comment2_by_id(comment2_id)
    print(comment2)
    if request.user.id == comment2.author.id:
        pass
    else:
        messages.warning(request, 'You have no permission to delete this comment!')
        return redirect('/')
    if request.method == 'POST':
        comment2.delete()
        return redirect(f'/article/{comment2.comment.article.id}')

def edit_description(request, user_id):
    if request.method == "POST":
        form_data = request.POST.dict()
        new_description = form_data["new_description"]
        user = request.user
        if contains_prohibited_words(new_description):
            messages.warning(request, 'Your new description contains profanity that is not allowed on our platform.\nPlease be polite!')
            return redirect(f'/profile/{request.user.id}')
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
            create_reaction_notification(sender=request.user, receiver=record.author, reaction_type='like')
            print(request.user.id, "-- тут")
        elif action == 'dislike':
            record.to_dislike(request.user.id)
            create_reaction_notification(sender=request.user, receiver=record.author, reaction_type='dislike')
    except Exception as e:
        print(e)
        resp_data = str(e)
    return redirect(f'/article/{article_id}')

def comment_reaction(request, action, comment_id):
    record = Comments_layer1.objects.get(pk=comment_id)
    try:
        if action == 'like':
            record.to_like(request.user.id)
            create_reaction_notification(sender=request.user, receiver=record.author, reaction_type='like')
            print(request.user.id, "-- тут")
        elif action == 'dislike':
            create_reaction_notification(sender=request.user, receiver=record.author, reaction_type='dislike')
            record.to_dislike(request.user.id)
    except Exception as e:
        print(e)
        resp_data = str(e)
    return redirect(f'/article/{record.article.id}')

def comment_reaction2(request, action, comment_id):
    record = Comments_layer2.objects.get(pk=comment_id)
    print(action)
    try:
        if action == 'like':
            record.to_like(request.user.id)
            print(request.user.id, "-- тут")
        elif action == 'dislike':
            record.to_dislike(request.user.id)
    except Exception as e:
        print(e)
        resp_data = str(e)
    return redirect(f'/article/{record.comment.article.id}')

def delete_article(request, article_id):
    article = get_article_by_id(article_id)
    if request.user.id == article.author.id:
        pass
    else:
        messages.warning(request, 'You have no permission to delete this article!')
        return redirect('/')
    if request.method == 'POST':
        article.delete()
        messages.success(request, message='Article successfully deleted!')
        return redirect('/')
    return render(request, 'deleting_article.html', context={'article': article})

def search(request):
    search_query = request.GET.get('query')
    articles = get_all_articles_by_search_query(search_query)
    return render(request, 'article_by_search_query.html', context={'articles': articles, "search_query": search_query})

