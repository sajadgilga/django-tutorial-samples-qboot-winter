from django.contrib import admin

from posts.models import Post, Comment


class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1


# @admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInlineAdmin]
    list_display = ['id', 'title', 'author_first_name', 'author', 'accepted']
    # exclude = ['accepted']
    search_fields = ['=title', 'id', 'author__username', 'author__first_name']
    list_filter = ['author', 'created_date', 'accepted']
    # fields = (('id', 'created_date'), ('author', 'title'), 'content')
    readonly_fields = ('id', 'created_date', 'author')
    fieldsets = (
        ('basic data', {'fields': [('id', 'created_date',), 'accepted']}),
        ('post info', {'fields': ['title', 'content', 'release_date']}),
    )
    actions = ['accept_posts']

    def author_first_name(self, post):
        return post.author.first_name

    def accept_posts(self, request, queryset):
        for obj in queryset:
            obj.accepted = True
            obj.save()


PostAdmin.accept_posts.short_description = 'My Custom Acceptance action'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created_date', 'status']
    list_filter = ['status']
    raw_id_fields = ['post']


admin.site.register(Post, PostAdmin)
