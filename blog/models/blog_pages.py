from datetime import datetime

from django import forms
from django.db import models

from modelcluster.fields import ParentalManyToManyField

from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.search import index
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page
import json

from blog.models.blog_tags import BlogPostTag


class BlogIndexPage(RoutablePageMixin, Page):
    header = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header', classname='full')
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndexPage, self).get_context(request)

        category = request.GET.get('category')

        blogposts = []
        if None != category and '' != category and 'None' != category:
            context['category'] = category
            categoryObj = BlogCategory.objects.get(name=category)
            context['category_description'] = categoryObj.description
            blogposts = self.get_children() \
                .filter(blogpost__categories__name=category)
        else:
            context['category'] = 'All News'
            context['category_description'] = ''
            blogposts =self.get_children()

        blogposts = blogposts.filter(content_type__model= 'blogpost').order_by('-first_published_at')

        paginator = Paginator(blogposts, 15) # Show 5 resources per page
        page = request.GET.get('page')
        try:
            resources = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            resources = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            resources = paginator.page(paginator.num_pages)

            # make the variable 'resources' available on the template
        paged_blogposts = []
        items = []
        count = 0
        for item in resources:
            items.append(item)
            count+=1
            if count % 3 == 0:
                paged_blogposts.append(items)
                items = []

        if items not in paged_blogposts:
            paged_blogposts.append(items)

        context['blogposts'] = paged_blogposts

        return context


class BlogPost(RoutablePageMixin, Page):
    date = models.DateTimeField("Post date", default=datetime.now)
    subtitle = models.CharField(max_length=250, blank=True)
    header_image = models.ForeignKey('wagtailimages.Image',
                                     on_delete=models.SET_NULL, related_name='+', blank=True, null=True, )

    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Post meta"),
        FieldPanel('subtitle'),
        FieldPanel('body', classname="full"),
        ImageChooserPanel('header_image'),
    ]

    @route(r'^$') # will override the default Page serving mechanism
    def post_view(self, request):
        tags = self.tags.all()
        categories = self.categories.all()
        discourse_topics = {'tags': {}, 'categories': {}}
        for cat in categories:
            cacheKey = cat.slug + '_category'
            data = cache.get(cacheKey)
            if data != None:
                discourse_topics['categories'][cat.slug] = data
        for tag in tags:
            cacheKey = tag.slug + '_tag'
            data = cache.get(cacheKey)
            if data != None:
                discourse_topics['tags'][tag.slug] = data
        self.discourse_topics = discourse_topics
        self.discourse_topics_json = json.dumps(discourse_topics)
        return super().serve(request)