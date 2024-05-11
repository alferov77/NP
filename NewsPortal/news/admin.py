from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Inline класс для PostCategory, чтобы управлять категориями из админки постов
class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1  # Количество пустых форм для добавления новых категорий

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'creation_date', 'post_type')
    list_filter = ('post_type', 'creation_date')
    search_fields = ('title', 'text')
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'author', 'post_type')
        }),
    )
    inlines = [PostCategoryInline]  # Добавление inline для категорий

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'creation_date', 'text')
    list_filter = ('creation_date', 'user')
    search_fields = ('text',)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment, CommentAdmin)
