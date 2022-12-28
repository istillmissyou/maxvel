from django.contrib import admin

from .models import CallMe, Contact, Link, User


class UserAdmin(admin.ModelAdmin):
    fields = [
        'password',
        'username',
    ]
    list_display = (
        'pk',
        'username',
        'password',
    )
    search_fields = ('username',)
    empty_value_display = '-пусто-'


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'phone',
        'address',
        'address_on_map',
        'email',
        # 'links',
    )


class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'link',
    )


class CallMeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'phone',
        'comment',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(CallMe, CallMeAdmin)
