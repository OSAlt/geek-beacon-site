from django.contrib import admin
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel

from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(default='')
    slug = models.SlugField(default='')
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'