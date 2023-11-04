from django.contrib import admin

from .models import Birthday, Tag


class BirthdayAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'birthday',
        'author',
    )


admin.site.register(Birthday, BirthdayAdmin)
admin.site.register(Tag)
