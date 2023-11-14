from datetime import timedelta

from .models import *
from django.contrib import messages
from django.db.models import Q

def get_tag_by_name(tag_name):
    return Tags.objects.get(name_of_topic=tag_name)

def get_tag_by_id(int_id):
    return Tags.objects.get(id=int_id)

def create_article_with_success_message(request, title, content, picture_url, user, tags):
    # article_data = form.save(commit=False)
    # article_data.author = request.user
    # article_data.publish()
    # messages.success(request, message='Article created!')
    new_article = Articles()
    new_article.title = title
    new_article.content = content
    new_article.author = user
    new_article.picture_url = picture_url
    new_article.user_id_number = user.pk
    new_article.status = 'clear'
    for tag in tags:
        try:
            db_tag = get_tag_by_name(tag)
        except:
                new_tag = Tags()
                new_tag.name_of_topic = tag
                new_tag.save()
                new_article.add_tag(tag)
        else:
            new_article.add_tag(tag)
    new_article.publish()
    messages.success(request, message='Article created!')

def create_comment_for_article(user, content, article_id):
    sender = user
    article = Articles.objects.get(pk=article_id)
    new_comment = Comments_layer1(author=user, content=content)
    new_comment.article = article
    new_comment.status = 'clear'
    new_comment.publish()
    if sender == article.author:
        pass
    else:
        new_notification = Comment_layer1_Notification(sender=sender, receiver=article.author, article=article, comment_content=new_comment)
        new_notification.publish()

def create_reaction_notification(sender, receiver, reaction_type):
    if sender == receiver:
        pass
    else:
        new_notification = Reaction_Notification(sender=sender, receiver=receiver, type_of_reaction=reaction_type)
        new_notification.publish()

def create_comment_layer1_notification(sender, article_id, comment_content):
    article = get_article_by_id(article_id)
    if sender == article.author:
        pass
    else:
        new_notification = Comment_layer1_Notification(sender=sender, receiver=article.author, article=article, comment_content=comment_content)
        new_notification.publish()

def create_comment_layer2_notification(sender, comment_id, comment_content):
    comment = get_comment_by_id(comment_id)
    if sender == comment.author:
        pass
    else:
        new_notification = Comment_layer2_Notification(sender=sender, receiver=comment.author, comment=comment, comment_content=comment_content)
        new_notification.publish()

def get_numeral_of_notifications_for_user(receiver):
    reaction_notifications = get_reaction_notifications(receiver)
    comment_l1_notifications = get_comment_layer1_notifications(receiver)
    comment_l2_notifications = get_comment_layer2_notifications(receiver)
    all_notifications = len(reaction_notifications) + len(comment_l1_notifications) + len(comment_l2_notifications)
    receiver.notifications = all_notifications
    receiver.save()

def get_comment_layer1_notifications(receiver):
    notifications = Comment_layer1_Notification.objects.all().filter(receiver=receiver)
    return notifications

def get_comment_layer2_notifications(receiver):
    notifications = Comment_layer2_Notification.objects.all().filter(receiver=receiver)
    return notifications

def get_reaction_notifications(receiver):
    notifications = Reaction_Notification.objects.all().filter(receiver=receiver)
    return notifications

def get_articles_from_subscriptions(list_of_subscriptions):
    articles = []
    for user_id in list_of_subscriptions:
        user_articles = get_all_articles_for_user(user_id)
        for article in user_articles:
            articles.append(article)
    return articles

def get_best_authors():
    all_users = CustomUser.objects.all()
    authors = []
    leader_board = {}
    best_authors = {}
    for user in all_users:
        user_articles = get_all_articles_for_user(user)
        if len(user_articles) == 0:
            pass
        else:
            authors.append(user)
    print(authors)
    for author in authors:
        sum_of_likes = get_sum_of_likes_for_user(author)
        leader_board[author.id] = sum_of_likes
    print(leader_board)
    for i in range(1, len(leader_board)+1):
        max_pair = max(leader_board.items(), key=lambda x: x[1])
        author = get_user_by_id(max_pair[0])
        best_authors[f'{i}'] = author
        leader_board.pop(max_pair[0])
    print(best_authors)
    return best_authors

def check_user_status(user_id):
    user = get_user_by_id(user_id)
    user_posts = get_all_articles_for_user(user)
    if len(user_posts) == 0:
        status = 'reader'
    else:
        status = 'author'
    return status


def get_sum_of_likes_for_user(user):
    user_articles = get_all_articles_for_user(user)
    sum_of_likes = 0
    for article in user_articles:
        for user_id in article.likes:
            if user_id == user.id:
                pass
            else:
                sum_of_likes = sum_of_likes + 1
    return sum_of_likes

def get_best_articles():
    articles = get_all_articles()
    best_articles = []
    for article in articles:
        if len(article.likes) > len(article.dislikes):
            best_articles.append(article)
        else:
            pass
    print(best_articles)
    return best_articles

def check_article_likes_amount(article, needed_amount):
    if len(article.likes) < int(needed_amount):
        return False
    elif len(article.likes) >= int(needed_amount):
        return True

def format_datetime(dt):
    # Преобразуйте дату и время в местное время
    local_dt = timezone.localtime(dt)

    # Форматируйте дату и время в желаемый формат
    formatted_datetime = local_dt.strftime('%b. %d, %Y, %I:%M %p')

    return formatted_datetime
def create_answer_for_comment(user, content, comment_id):
    sender = user
    comment = Comments_layer1.objects.get(pk=comment_id)
    new_answer = Comments_layer2(author=user, content=content)
    new_answer.comment = comment
    new_answer.status = 'clear'
    new_answer.publish()
    if sender == comment.author:
        pass
    else:
        new_notification = Comment_layer2_Notification(sender=sender, receiver=comment.author, comment=comment, comment_content=new_answer)
        new_notification.publish()

def delete_notification(notification_type, notification_id):
    notification = notification_type.objects.get(pk=notification_id)
    notification.close_notification()

def edit_pfp_for_user(user, profile_photo):
    user.profile_picture = profile_photo
    user.save()

def get_comment_by_id(comment_id):
    return Comments_layer1.objects.get(pk=comment_id)

def get_comment2_by_id(comment_id):
    return Comments_layer2.objects.get(pk=comment_id)

def create_review(request, review_content, number_of_stars):
    new_feedback = Feedbacks(author=request.user,
                             content=review_content,
                             number_of_stars=int(number_of_stars))
    new_feedback.publish()
    messages.success(request, message='Thanks for your feedback!')

def get_other_comments(comment_id):
    comment = Comments_layer1.objects.get(pk=comment_id)
    comments = Comments_layer2.objects.all().filter(comment=comment)
    return comments

def get_user_by_id(user_id):
    return CustomUser.objects.get(pk=user_id)

def to_subscribe(request, user2):
    if request.user.id in user2.subscribers and user2.id in request.user.subscriptions:
        user2.subscribers.remove(request.user.id)
        request.user.subscriptions.remove(user2.id)
    else:
        user2.subscribers.append(request.user.id)
        request.user.subscriptions.append(user2.id)
    user2.save()
    request.user.save()
    print(user2.subscribers)
    print(request.user.subscriptions)

def get_all_preferences():
    return Tags.objects.all()

def get_all_articles_for_user(user):
    return Articles.objects.all().filter(author=user)

def get_all_articles():
    return Articles.objects.all()

def get_article_by_id(article_id):
    return Articles.objects.get(pk=article_id)

def get_user_info_by_id(user_id):
    return User.objects.get(id=user_id)

def add_preference(preference, user_id):
    user_container = get_user_info_by_id(user_id)
    user_container.preferences.append(preference)
    user_container.save()

def edit_description_for_user(user, new_description):
    user.about_user = new_description
    user.save()

def get_comments_for_article(article_id):
    article = get_article_by_id(article_id)
    return Comments_layer1.objects.all().filter(article=article)

def get_all_articles_by_search_query(search_query):
    return Articles.objects.filter(Q(content__icontains=search_query) or Q(content__icontains=search_query))



# def get_all_questions_with_answers():
#     return Question.objects.all().prefetch_related('answer_set')


def get_articles_published_last_hour():
    # Calculate the datetime one hour ago from the current time
    one_hour_ago = timezone.now() - timedelta(days=5)

    # Query the Articles model to get articles published within the last hour
    articles_published_last_hour = Articles.objects.filter(published_date__gte=one_hour_ago)
    return articles_published_last_hour