import os
import requests
from celery import shared_task
import django
from django.apps import apps
from django.core.cache import cache

os.environ['DJANGO_SETTINGS_MODULE'] = 'geekbeacon.settings.dev'
django.setup()
BlogPostTag = apps.get_model('blog', 'BlogPostTag')
BlogCategory = apps.get_model('blog', 'BlogCategory')

@shared_task
def get_discourse_topics():
    get_discourse_tag_topics()
    get_discourse_category_topics()
# gets the top posts from discourse by tag
def get_discourse_tag_topics():
    tags = BlogPostTag.objects.distinct('tag')

    for t in tags:
        # gets 30 recent active discourse forum topics for that tag and cache them
        url = 'https://forum.geekbeacon.org/tags/' + t.tag.slug + '.json'
        r = requests.get(url)
        data = r.json()
        if 'error_type' in data:
            print("tag was not found: not_found")
        else:
            # cache the topic data
            cacheKey = t.tag.slug + '_tag'
            cache.set(cacheKey, data['topic_list']['topics'], None)

def get_discourse_category_topics():
    blogCategories = BlogCategory.objects.all()
    categoriesRequest = requests.get('https://forum.geekbeacon.org/categories.json')
    discourseCategories = categoriesRequest.json()
    discourseCategories = discourseCategories['category_list']['categories']
    slugIdDict = {}
    for category in discourseCategories:
        slugIdDict[category['slug']] = category['id']
    for blogCategory in blogCategories:
        # check if theres a discourse category that matches and get topics
        if blogCategory.slug in slugIdDict:
            categoryTopicsRequest = requests.get('https://forum.geekbeacon.org/c/' + str(slugIdDict[blogCategory.slug]) + '.json')
            categoryTopics = categoryTopicsRequest.json()
            if 'error_type' in categoryTopics:
                print("category was not found: not_found")
            else:
                # cache the topic data
                cacheKey = blogCategory.slug + '_category'
                cache.set(cacheKey, categoryTopics['topic_list']['topics'], None)
