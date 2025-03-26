from django.shortcuts import render
from .utils import get_user_activity

def analytics(request):
    activity_dates, activity_counts = get_user_activity()
    """
    feature_usage = FeatureUsage.objects.all()
    feature_name = [feature.name for feature in feature_usage]
    feature_usage = [feature.usage_count for feature in feature_usage]

    gender_count = GenderCount.objects.first()
    female_count = gender_count.female_count if gender_count else 0
    male_count = gender_count.male_count if gender_count else 0

    engagement_type = EngagementType.objects.first()
    follow_count = engagement_type.follow_count if engagement_type else 0
    comment_count = engagement_type.comment_count if engagement_type else 0
    like_count = engagement_type.like_count if engagement_type else 0

    insights = Insights.objects.first()
    highest_active_users = insights.highest_active_users if insights else 0
    total_accounts = insights.total_accounts if insights else 0
    most_used_feature = insights.most_used_feature if insights else ""
    total_itineraries = insights.total_itineraries if insights else 0
    avg_itineraries_per_user = insights.avg_itineraries_per_user if insights else 0.0
    avg_journey_duration_days = insights.avg_journey_duration.days if insights else 0
    """

    data = {
        'activity_dates': [date.strftime('%Y-%m-%d') for date in activity_dates],
        'activity_counts': activity_counts,
        #'female_count': female_count,
        #'male_count': male_count,
        #'feature_name': feature_name,
        #'feature_usage': feature_usage,
        #'follow_count': follow_count,
        #'comment_count': comment_count,
        #'like_count': like_count,
        #'highest_active_users': highest_active_users,
        #'total_accounts': total_accounts,
        #'most_used_feature': most_used_feature,
        #'total_itineraries': total_itineraries,
        #'avg_itineraries_per_user': avg_itineraries_per_user,
        #'avg_journey_duration': avg_journey_duration_days,
    }
    return render(request, 'analytics.html', data)

def monitor(request):
    return render(request, 'monitor.html')