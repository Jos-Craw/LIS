from django.contrib import admin
import datetime

from .models import AdvUser, Post, Comment, Consult, Section, Tvor, Trud,Volant , Vist, Event, PostType


class PostAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'content', 'author', 'pubdate','tags', 'image','stoim','mesta','mesta_now', 'file', 'video', 'audio','eventtime','eventdate')
    list_display_links = ('content','name',)
    search_fields = ('name','content', 'author','tags','eventtime','eventdate','stoim','mesta','mesta_now', 'image', 'file', 'video', 'audio')
    date_hierarchy = 'pubdate'
    fields = ('name','author','tags', 'content','eventtime','eventdate', 'image','stoim','mesta','mesta_now', 'file', 'video', 'audio')


admin.site.register(Post, PostAdmin)

class VistAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'content', 'author', 'pubdate', 'image','stoim', 'file', 'video', 'audio','start_date','final_date')
    list_display_links = ('content','name',)
    search_fields = ('name', 'content', 'author', 'image','stoim', 'file', 'video', 'audio','event','start_date','final_date')
    date_hierarchy = 'pubdate'
    fields = ('name', 'content', 'author', 'image','stoim', 'file', 'video', 'audio','event','start_date','final_date')


admin.site.register(Vist, VistAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','eventtime','eventdate','zan','group')
    search_fields = ('id','eventtime','eventdate','zan','zapisi','group')
    fields = ('eventtime','eventdate','zan','zapisi','group')

admin.site.register(Event, EventAdmin)

class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('id','post','user','zap_type','colvo')
    search_fields = ('post','user')
    fields = ('post','user','zap_type','colvo')

admin.site.register(PostType, PostTypeAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'pubdate', 'post','vist', 'moderation')
    list_display_links = ('content',)
    search_fields = ('content', 'author')
    date_hierarchy = 'pubdate'
    fields = ('author', 'content', 'post','vist', 'moderation')


admin.site.register(Comment, CommentAdmin)

class ConsultAdmin(admin.ModelAdmin):
    list_display = ('eventdate', 'eventtime','zan')
    search_fields = ('eventdate', 'eventtime','zan')
    fields = ('eventdate', 'eventtime','zan')


admin.site.register(Consult, ConsultAdmin)


class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('id','__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'avatar', 'email', 'first_name', 'last_name','phone_num','faculty','group')
    fields = (('username', 'email', 'avatar','phone_num'), ('first_name', 'last_name'),('faculty','group'),
              ('is_active', 'is_activated'), ('is_staff', 'is_superuser'),
              'groups', 'user_permissions', ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')


admin.site.register(AdvUser, AdvUserAdmin)


class SectionAdmin(admin.ModelAdmin):
    list_display= ('name','otobr')
    search_fields = ('name','otobr')
    fields = ('name','otobr')

admin.site.register(Section, SectionAdmin)

class TvorAdmin(admin.ModelAdmin):
    list_display= ('name','otobr')
    search_fields = ('name','otobr')
    fields = ('name','otobr')

admin.site.register(Tvor, TvorAdmin)

class TrudAdmin(admin.ModelAdmin):
    list_display= ('name','otobr')
    search_fields = ('name','otobr')
    fields = ('name','otobr')

admin.site.register(Trud, TrudAdmin)

class VolantAdmin(admin.ModelAdmin):
    list_display= ('name','otobr')
    search_fields = ('name','otobr')
    fields = ('name','otobr')

admin.site.register(Volant, VolantAdmin)
