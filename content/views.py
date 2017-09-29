from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from content.models import ContentItem, ContentTag, PublishHistory, FeatureHistory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from content.view_utils import *
from .forms import AddContentForm, AddMenuItemForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test

def is_editor(request):
    return self.user.groups.filter(name__in=['onetime','monthtime']).exists()


class HomePage(View):
    """Home page view"""

    def get(self, request):
        # Get the menu
        menu = get_menu_items()

        # Get the latest content for sidebar and footer
        latest_content = get_latest_content()

        # Render the view
        return render(request, "pages/home.html",
                                            {"latest_content" : latest_content,
                                             "menu" : menu,})


class ContentDisplay(View):
    """Single item display"""

    def get(self, request, content_id):
        # Get the menu
        menu = get_menu_items()

        # Query the DB for content by ID
        content = ContentItem.objects.get(pk=content_id)

        # Get the latest content for sidebar and footer
        latest_content = get_latest_content()

        # Get the latest featured content
        featured_content = get_featured_content()

        # get all tags for sidebar
        tags = ContentTag.objects.all()

        # Set the layout based on the content's layout value
        layout = layout_selector(content.layout.selected)

        # Render the view
        return render(request, layout, {"content" : content,
                                        "latest_content" : latest_content,
                                        "featured_content" : featured_content,
                                        "tags" : tags,
                                        "menu" : menu,})


class ContentDisplayList(View):
    """List recent posts of tag type (default all tags)"""

    def get(self, request, tag=None):
        if tag:
            # If there is a tag, query the database with it
            posts = ContentItem.objects.filter(content_type__selected='post').filter(tags__name=tag).order_by('updated_at')
            title = tag
        else:
            # If there is no tag, query the database for all posts
            posts = ContentItem.objects.filter(content_type__selected='post').order_by('updated_at')
            title = "Recent Posts"

        # Paginate the posts object and show 5 posts per page
        paginator = Paginator(posts, 5)

        # Get the page number from the request url (?page=)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        # Get the menu
        menu = get_menu_items()

        # Get the latest content for sidebar and footer
        latest_content = get_latest_content()

        # Get the latest featured content
        featured_content = get_featured_content()

        # Get the tags that exist in the database
        tags = ContentTag.objects.all()

        # Render the view
        return render(request, "pages/content/content_base.html",
                                                            {"title" : title,
                                                            "posts" : posts,
                                                            "latest_content" : latest_content,
                                                            "featured_content" : featured_content,
                                                            "tags" : tags,
                                                            "menu" : menu,})




class ContentAdminHome(UserPassesTestMixin, LoginRequiredMixin, View):
    """Content Administrator Home View"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Editor',])

    def get(self, request, operation=None):

        menu = get_menu_items()
        content = ContentItem.objects.all()
        return render(request, "pages/content/admin/content_admin.html",{"menu": menu,
                                                                         "content" : content})

class MenuAdminHome(UserPassesTestMixin, LoginRequiredMixin, View):
    """Menu Administrator Home View"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Editor',])

    def get(self, request, operation=None):

        menu = get_menu_items()
        content = MenuItem.objects.all()
        return render(request, "pages/content/admin/menu/menu_admin.html",{"menu": menu,
                                                                         "content" : content})


class AddMenuItem(UserPassesTestMixin, LoginRequiredMixin, View):
    """View to Add Menu Items"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Editor',])

    def get(self, request, operation=None):

        menu = get_menu_items()
        form = AddMenuItemForm()
        return render(request, "pages/content/admin/menu/menu_item_add.html",{"form": form,
                                                                         "menu" : menu})

    def post(self, request, operation=None):
        form = AddMenuItemForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            menu_item = MenuItem()

            menu_item.parent = form.cleaned_data['parent']
            menu_item.content = form.cleaned_data['content']
            menu_item.title = form.cleaned_data['title']
            menu_item.override_url = form.cleaned_data['override_url']
            menu_item.priority = form.cleaned_data['priority']
            menu_item.published = form.cleaned_data['published']

            menu_item.save()


            return HttpResponseRedirect('/content/menu/admin/')


class AddContent(UserPassesTestMixin, LoginRequiredMixin, View):
    """View to Add Content"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Editor',])

    def get(self, request):

        menu = get_menu_items()
        form = AddContentForm()
        return render(request, "pages/content/admin/add_content.html",{"form": form,
                                                                         "menu" : menu})

    def post(self, request):
        form = AddContentForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            from django.db import models
            try:
                content = ContentItem()
            except Exception as e:
                print(e)
            print('hi')
            print(form.cleaned_data['header_image'])
            print(form.cleaned_data['thumbnail_image'])
            print('hello')
            content.title = form.cleaned_data['title']
            content.author = form.cleaned_data['author']
            content.header_image = form.cleaned_data['header_image']
            content.thumbnail_image = form.cleaned_data['thumbnail_image']
            content.description = form.cleaned_data['description']
            content.body = form.cleaned_data['body']
            content.category = form.cleaned_data['category']
            content.layout = form.cleaned_data['layout']
            content.content_type = form.cleaned_data['content_type']
            content.save()
            content.tags = form.cleaned_data['tags']
            content.save()

            published = PublishHistory()
            published.content_item = ContentItem.objects.get(id=content.id)
            published.published = form.cleaned_data['published']
            published.save()

            featured = FeatureHistory()
            featured.content_item = ContentItem.objects.get(id=content.id)
            featured.featured = form.cleaned_data['featured']
            featured.image = form.cleaned_data['featured_image']
            featured.save()

            return HttpResponseRedirect('/content/admin/')


class EditMenuItem(UserPassesTestMixin, LoginRequiredMixin, View):
    """View to Add Menu Items"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Editor',])

    def get(self, request, menu_item_id=None):

        menu = get_menu_items()

        content = MenuItem.objects.get(pk=menu_item_id)

        form = AddMenuItemForm(initial={'title': content.title,
                                        'content': content.content,
                                        'parent': content.parent,
                                        'override_url': content.override_url,
                                        'priority': content.priority,
                                        'published': content.published,
                                        })

        return render(request, "pages/content/admin/menu/menu_item_edit.html",{"form": form,
                                                                             "menu" : menu,
                                                                             "menu_item_id" : menu_item_id})

    def post(self, request, menu_item_id=None):
        form = AddMenuItemForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():

            # process the data in form.cleaned_data as required
            try:
                menu_item = MenuItem(pk=menu_item_id)
            except Exception as e:
                print(e)

            menu_item.parent = form.cleaned_data['parent']
            menu_item.content = form.cleaned_data['content']
            menu_item.title = form.cleaned_data['title']
            menu_item.override_url = form.cleaned_data['override_url']
            menu_item.priority = form.cleaned_data['priority']
            menu_item.published = form.cleaned_data['published']

            menu_item.save()

            return HttpResponseRedirect('/content/menu/admin/')


class EditContent(UserPassesTestMixin, LoginRequiredMixin, View):
    """View to Add Content"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Editor',])

    def get(self, request, content_id=None):

        menu = get_menu_items()
        content = ContentItem.objects.get(pk=content_id)
        try:
            published = PublishHistory.objects.filter(content_item=content_id).order_by('updated_at')
            published = published[0].published
        except:
            published = False
        try:
            result = FeatureHistory.objects.filter(content_item__id=content_id).order_by('updated_at')
            featured = result[0].featured
            featured_image = result[0].image
        except:
            featured = False
            featured_image = None

        form = AddContentForm(initial={'title': content.title,
                                        'description': content.description,
                                        'body': content.body,
                                        'author': content.author,
                                        'category': content.category,
                                        'tags': content.tags.all,
                                        'layout': content.layout,
                                        'content_type': content.content_type,
                                        'published': published,
                                        'featured': featured,
                                        'header_image': content.header_image,
                                        'thumbnail_image': content.thumbnail_image,
                                        'featured_image': featured_image,})

        return render(request, "pages/content/admin/edit_content.html",{"form": form,
                                                                         "menu" : menu,
                                                                         "content_id" : content_id})

    def post(self, request, content_id=None):
        form = AddContentForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            content, created = ContentItem.objects.get_or_create(id=content_id)

            content.title = form.cleaned_data['title']
            content.header_image = form.cleaned_data['header_image']
            content.thumbnail_image = form.cleaned_data['thumbnail_image']
            content.description = form.cleaned_data['description']
            content.body = form.cleaned_data['body']
            content.author = form.cleaned_data['author']
            content.category = form.cleaned_data['category']
            content.tags = form.cleaned_data['tags']
            content.layout = form.cleaned_data['layout']
            content.content_type = form.cleaned_data['content_type']
            content.save()

            published, created = PublishHistory.objects.get_or_create(content_item__id=content_id, defaults={'published': False, 'content_item_id':content_id})
            published.published = form.cleaned_data['published']
            published.save()

            featured, created = FeatureHistory.objects.get_or_create(content_item__id=content_id, defaults={'featured': False, 'content_item_id':content_id})
            featured.content_item = ContentItem.objects.get(pk=content_id)
            featured.featured = form.cleaned_data['featured']
            featured.image = form.cleaned_data['featured_image']
            featured.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/content/admin/')


class DeleteContentItem(UserPassesTestMixin, LoginRequiredMixin, View):
    """View to Add Content"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Editor',])

    def get(self, request, content_id=None):

        menu = get_menu_items()
        content = ContentItem.objects.get(pk=content_id)
        content.delete()
        return HttpResponseRedirect('/content/admin/')

class DeleteMenuItem(UserPassesTestMixin, LoginRequiredMixin, View):
    """View to Add Content"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=['Editor',])

    def get(self, request, menu_item_id=None):

        menu = get_menu_items()
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        menu_item.delete()
        return HttpResponseRedirect('/content/menu/admin/')
