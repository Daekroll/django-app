

from django.contrib import admin

from .models import Article, Tag, Author, Category


class TagInLine(admin.StackedInline):
    model = Article.tags.through
    extra = 0


# class AuthorInLine(admin.TabularInline):
#     model = Article.author.through
#     extra = 0
#
#
# class CategoryInLine(admin.TabularInline):
#     model = Article.category.through
#     extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        TagInLine,
    ]
    list_display = 'pk', 'title', 'content', 'pub_date', 'author', 'category'
    list_display_links = 'pk', 'title',

    def get_queryset(self, request):
        return Article.objects.select_related('author', 'category').prefetch_related('tags')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name', 'bio',
    list_display_links = 'pk', 'name',


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name',
    list_display_links = 'pk', 'name',


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'pk', 'name',
    list_display_links = 'pk', 'name',
