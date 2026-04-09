from django.db import models
from django.utils import timezone

class ScanResult(models.Model):
    url = models.URLField(max_length=500)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Store issues as a JSON payload for flexibility
    issues_payload = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.url} - {self.score} ({self.created_at.strftime('%Y-%m-%d')})"

class UserPreference(models.Model):
    user_hash = models.CharField(max_length=255, unique=True, help_text="Anonymous identifier")
    high_contrast_default = models.BooleanField(default=False)
    voice_narration_speed = models.FloatField(default=1.0)
    
    def __str__(self):
        return f"Preferences for {self.user_hash[:8]}"
