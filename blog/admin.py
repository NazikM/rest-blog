from django.contrib import admin

from blog.models import Category, Article


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created', 'modified')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
