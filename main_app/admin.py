# main_app/admin.py

from django.contrib import admin
from .models import Practice, Registration

class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0
    readonly_fields = ('user', 'practice', 'registered_at')
    can_delete = True
    verbose_name = '参加登録'
    verbose_name_plural = '参加登録一覧'

class PracticeAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'is_closed', 'max_participants', 'current_participants')
    list_filter = ('is_closed', 'date')
    search_fields = ('location',)
    inlines = [RegistrationInline]
    
    def current_participants(self, obj):
        return obj.registration_set.count()
    current_participants.short_description = '登録者数'

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'practice', 'registered_at')
    list_filter = ('practice', 'registered_at')
    search_fields = ('user__username', 'practice__location')
    raw_id_fields = ('user', 'practice')

admin.site.register(Practice, PracticeAdmin)
admin.site.register(Registration, RegistrationAdmin)
