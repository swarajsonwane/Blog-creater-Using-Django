from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
#This is to show more details for admin
class PostAdmin(admin.ModelAdmin):
    #to display info
    list_display = ('title', 'slug', 'author', 'publish',
                       'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

@admin.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','created','post','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')


#
#
# class PostAdmin(admin.ModelAdmin):
#     #to display info
#     list_display = ('title', 'slug', 'author', 'publish',
#                        'status')
#     #added filter to right side of admin
#     list_filter = ('status', 'created', 'publish', 'author')
#     #search bar for searcing title or body
#     search_fields = ('title', 'body')
#     #auto adding slug for fields
#     prepopulated_fields = {'slug': ('title',)}
#
#     raw_id_fields = ('author',)
#     date_hierarchy = 'publish'
#     #ordered accor to
#     ordering = ('status', 'publish')