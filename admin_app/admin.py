from django.contrib import admin
from .models import UserActivity, FeatureUsage, GenderDistribution, EngagementMetrics, DashboardInsights

admin.site.register(UserActivity)
admin.site.register(FeatureUsage)
admin.site.register(GenderDistribution)
admin.site.register(EngagementMetrics)
admin.site.register(DashboardInsights)