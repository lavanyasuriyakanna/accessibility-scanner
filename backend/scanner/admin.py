from django.contrib import admin
from .models import ScanResult, UserPreference

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('url', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('url',)

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user_hash', 'high_contrast_default', 'voice_narration_speed')
