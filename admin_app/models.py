from django.db import models
from django.conf import settings
from django.utils import timezone

# Models for analytics data (Atheen)
# Count active users daily
class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    # Delete activity older than 7 days
    def save(self, *args, **kwargs):
        old = timezone.now() - timezone.timedelta(days=7)
        UserActivity.objects.filter(date__lt=old).delete()
        super().save(*args, **kwargs)
        
"""
# Record feature clicks
class FeatureUsage(models.Model):
    feature_name = models.CharField(unique=True)
    click_count = models.PositiveIntegerField(default=0)
"""