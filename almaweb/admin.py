from django.contrib import admin
from django.contrib import admin
from .models import Article
from .models import News
from .models import Comment
from core.admin import custom_admin_site



class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)

custom_admin_site.register(Article, ArticleAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    
custom_admin_site.register(News, NewsAdmin)


class JournalAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_posted')

custom_admin_site.register(Comment, JournalAdmin)