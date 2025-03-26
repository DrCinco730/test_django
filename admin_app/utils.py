from datetime import timedelta
from .models import UserActivity
from django.utils import timezone
from django.db.models import Count

# Retrieve user activity over the past 7 days (Atheen)
def get_user_activity():
    today = timezone.now().date()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]
    activity = {date: 0 for date in dates}

    # Query DB for user activity
    user_activity = (
        UserActivity.objects
        .filter(date__date__gte=dates[0])
        .values('date__date')
        .annotate(count=Count('user', distinct=True))
    )
    # Return a list of dates and another of counts
    for entry in user_activity:
        activity[entry['date__date']] = entry['count']
    return list(activity.keys()), list(activity.values())
