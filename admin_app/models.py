from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


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


# Record feature clicks
class FeatureUsage(models.Model):
    feature_name = models.CharField(max_length=100, unique=True)
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.feature_name}: {self.click_count} clicks"


# Track gender distribution
class GenderDistribution(models.Model):
    # Only one row will exist in this table - it's a singleton
    female_count = models.PositiveIntegerField(default=0)
    male_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Gender Distribution (F: {self.female_count}, M: {self.male_count})"

    @classmethod
    def update_counts(cls):
        """Update gender counts from UserProfile data"""
        from user_app.models import UserProfile

        female_count = UserProfile.objects.filter(gender='F').count()
        male_count = UserProfile.objects.filter(gender='M').count()

        obj, created = cls.objects.get_or_create(pk=1)
        obj.female_count = female_count
        obj.male_count = male_count
        obj.save()

        return obj


# Track engagement types
class EngagementMetrics(models.Model):
    # Only one row will exist in this table - it's a singleton
    follow_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Engagement Metrics (updated: {self.last_updated.strftime('%Y-%m-%d')})"


# Dashboard insights
class DashboardInsights(models.Model):
    # Only one row will exist in this table - it's a singleton
    highest_active_users = models.PositiveIntegerField(default=0)
    total_accounts = models.PositiveIntegerField(default=0)
    most_used_feature = models.CharField(max_length=100, blank=True)
    total_itineraries = models.PositiveIntegerField(default=0)
    avg_itineraries_per_user = models.FloatField(default=0.0)
    avg_journey_duration = models.PositiveIntegerField(default=0)  # In days
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dashboard Insights (updated: {self.last_updated.strftime('%Y-%m-%d')})"

    @classmethod
    def update_insights(cls):
        """Update dashboard insights with current data"""
        # Get total accounts
        total_accounts = User.objects.count()

        # Get most used feature
        most_used = FeatureUsage.objects.order_by('-click_count').first()
        most_used_feature = most_used.feature_name if most_used else ""

        # Get highest active users in a day
        from django.db.models import Count
        from datetime import timedelta

        # Group by date and count users
        user_counts = UserActivity.objects.values('date__date').annotate(
            user_count=Count('user', distinct=True)
        ).order_by('-user_count')

        highest_active = user_counts.first()
        highest_active_users = highest_active['user_count'] if highest_active else 0

        # For now, set placeholder values for itineraries
        # These would be updated when the Trip model is implemented
        total_itineraries = 0
        avg_itineraries_per_user = 0.0
        avg_journey_duration = 0

        obj, created = cls.objects.get_or_create(pk=1)
        obj.total_accounts = total_accounts
        obj.most_used_feature = most_used_feature
        obj.highest_active_users = highest_active_users
        obj.total_itineraries = total_itineraries
        obj.avg_itineraries_per_user = avg_itineraries_per_user
        obj.avg_journey_duration = avg_journey_duration
        obj.save()

        return obj


class Traveler(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    settings = models.JSONField(default=dict)  # For storing offline mode, notification preferences etc.

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class POI(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='points_of_interest')
    description = models.TextField()
    location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='poi_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Point of Interest"
        verbose_name_plural = "Points of Interest"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


# تعديل نموذج Trip
class Trip(models.Model):
    name = models.CharField(max_length=200)
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name='trips')
    start_date = models.DateField()
    end_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='trips')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    collaborators = models.ManyToManyField(Traveler, related_name='collaborated_trips')
    points_of_interest = models.ManyToManyField(POI, related_name='trips', blank=True)
    location = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.traveler.user.username}"


class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='itineraries')
    location = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.trip.name} - {self.location}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('system', 'System Notification'),
        ('trip', 'Trip Reminder')
    ]

    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    notification_date = models.DateTimeField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.traveler.user.username}"


class CalendarSync(models.Model):
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name='calendar_syncs')
    device_id = models.CharField(max_length=200)
    calendar_data = models.JSONField()
    sync_date = models.DateTimeField()
    sync_status = models.CharField(max_length=50)  # success, failed, etc.

    def __str__(self):
        return f"Calendar sync for {self.traveler.user.username}"


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('new', 'جديد'),
        ('in_progress', 'قيد المعالجة'),
        ('resolved', 'تم الحل'),
        ('closed', 'مغلق')
    ]

    PRIORITY_CHOICES = [
        ('low', 'منخفضة'),
        ('medium', 'متوسطة'),
        ('high', 'عالية'),
        ('urgent', 'عاجلة')
    ]

    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tickets')

    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"


class TicketResponse(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff_response = models.BooleanField(default=False)

    def __str__(self):
        return f"Response to ticket #{self.ticket.id}"


class TravelerNote(models.Model):
    traveler = models.ForeignKey(Traveler, on_delete=models.CASCADE, related_name='admin_notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.traveler.user.username}"


# تحديث نموذج Traveler لإضافة المزيد من المعلومات
class TravelerVerification(models.Model):
    VERIFICATION_STATUS = [
        ('pending', 'قيد المراجعة'),
        ('verified', 'تم التحقق'),
        ('rejected', 'مرفوض')
    ]

    traveler = models.OneToOneField(Traveler, on_delete=models.CASCADE, related_name='verification')
    id_document = models.FileField(upload_to='verification_docs/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=VERIFICATION_STATUS, default='pending')
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Verification for {self.traveler.user.username}"