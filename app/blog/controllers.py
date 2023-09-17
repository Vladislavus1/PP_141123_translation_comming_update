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
    new_comment = Comments_layer1(author=user, content=content)
    new_comment.article = Articles.objects.get(pk=article_id)
    new_comment.publish()

def format_datetime(dt):
    # Преобразуйте дату и время в местное время
    local_dt = timezone.localtime(dt)

    # Форматируйте дату и время в желаемый формат
    formatted_datetime = local_dt.strftime('%b. %d, %Y, %I:%M %p')

    return formatted_datetime
def create_answer_for_comment(user, content, comment_id):
    new_answer = Comments_layer2(author=user, content=content)
    new_answer.comment = Comments_layer1.objects.get(pk=comment_id)
    new_answer.publish()

def edit_pfp_for_user(user, profile_photo):
    user.profile_picture = profile_photo
    user.save()

def get_comment_by_id(comment_id):
    return Comments_layer1.objects.get(pk=comment_id)

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

def get_all_new_articles():
    return Articles.objects.all().filter()

# def get_all_questions_with_answers():
#     return Question.objects.all().prefetch_related('answer_set')


def get_articles_published_last_hour():
    # Calculate the datetime one hour ago from the current time
    one_hour_ago = timezone.now() - timedelta(days=5)

    # Query the Articles model to get articles published within the last hour
    articles_published_last_hour = Articles.objects.filter(published_date__gte=one_hour_ago)
    print()
    return articles_published_last_hour