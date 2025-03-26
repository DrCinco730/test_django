# # from django.shortcuts import render
# # from .utils import get_user_activity
# #
# # def analytics(request):
# #     activity_dates, activity_counts = get_user_activity()
# #     """
# #     feature_usage = FeatureUsage.objects.all()
# #     feature_name = [feature.name for feature in feature_usage]
# #     feature_usage = [feature.usage_count for feature in feature_usage]
# #
# #     gender_count = GenderCount.objects.first()
# #     female_count = gender_count.female_count if gender_count else 0
# #     male_count = gender_count.male_count if gender_count else 0
# #
# #     engagement_type = EngagementType.objects.first()
# #     follow_count = engagement_type.follow_count if engagement_type else 0
# #     comment_count = engagement_type.comment_count if engagement_type else 0
# #     like_count = engagement_type.like_count if engagement_type else 0
# #
# #     insights = Insights.objects.first()
# #     highest_active_users = insights.highest_active_users if insights else 0
# #     total_accounts = insights.total_accounts if insights else 0
# #     most_used_feature = insights.most_used_feature if insights else ""
# #     total_itineraries = insights.total_itineraries if insights else 0
# #     avg_itineraries_per_user = insights.avg_itineraries_per_user if insights else 0.0
# #     avg_journey_duration_days = insights.avg_journey_duration.days if insights else 0
# #     """
# #
# #     data = {
# #         'activity_dates': [date.strftime('%Y-%m-%d') for date in activity_dates],
# #         'activity_counts': activity_counts,
# #         #'female_count': female_count,
# #         #'male_count': male_count,
# #         #'feature_name': feature_name,
# #         #'feature_usage': feature_usage,
# #         #'follow_count': follow_count,
# #         #'comment_count': comment_count,
# #         #'like_count': like_count,
# #         #'highest_active_users': highest_active_users,
# #         #'total_accounts': total_accounts,
# #         #'most_used_feature': most_used_feature,
# #         #'total_itineraries': total_itineraries,
# #         #'avg_itineraries_per_user': avg_itineraries_per_user,
# #         #'avg_journey_duration': avg_journey_duration_days,
# #     }
# #     return render(request, 'analytics.html', data)
# #
# # def monitor(request):
# #     return render(request, 'monitor.html')
#
#
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth.models import User
# from django.db.models import Count
# from django.utils import timezone
# from django.contrib import messages
# from django.http import HttpResponseForbidden, HttpResponseRedirect
# from datetime import timedelta
# from user_app.models import UserProfile
#
# from .utils import get_user_activity
# from .models import UserActivity, FeatureUsage, GenderDistribution, EngagementMetrics, DashboardInsights
#
#
# # التحقق مما إذا كان المستخدم مسؤولاً
# def is_staff(user):
#     return user.is_staff
#
#
# @login_required
# @user_passes_test(is_staff)
# def analytics(request):
#     """عرض صفحة التحليلات والإحصائيات"""
#     # الحصول على بيانات نشاط المستخدمين
#     activity_dates, activity_counts = get_user_activity()
#
#     # قيم افتراضية في حالة عدم وجود نماذج
#     feature_names = []
#     feature_usage_counts = []
#     female_count = 0
#     male_count = 0
#     follow_count = 0
#     comment_count = 0
#     like_count = 0
#     highest_active_users = 0
#     total_accounts = User.objects.count()  # على الأقل يمكننا حساب المستخدمين
#     most_used_feature = ""
#     total_itineraries = 0
#     avg_itineraries_per_user = 0
#     avg_journey_duration = 0
#
#     # الحصول على بيانات استخدام الميزات
#     feature_usages = FeatureUsage.objects.all().order_by('-click_count')[:5]  # أعلى 5 ميزات
#     if feature_usages:
#         feature_names = [feature.feature_name for feature in feature_usages]
#         feature_usage_counts = [feature.click_count for feature in feature_usages]
#
#     # إذا لم توجد بيانات استخدام ميزات، أنشئ بيانات افتراضية
#     if not feature_usages:
#         default_features = ['Profile', 'Explore', 'Trips', 'Favorites', 'Map']
#         for i, feature in enumerate(default_features):
#             FeatureUsage.objects.get_or_create(
#                 feature_name=feature,
#                 defaults={'click_count': (i + 1) * 2}
#             )
#         # إعادة جلب البيانات بعد الإنشاء
#         feature_usages = FeatureUsage.objects.all().order_by('-click_count')[:5]
#         feature_names = [feature.feature_name for feature in feature_usages]
#         feature_usage_counts = [feature.click_count for feature in feature_usages]
#
#     # الحصول على توزيع النوع
#     gender_dist = GenderDistribution.objects.first()
#     if not gender_dist:
#         # تحديث إحصاءات النوع من ملفات تعريف المستخدمين
#         female_count = UserProfile.objects.filter(gender='F').count()
#         male_count = UserProfile.objects.filter(gender='M').count()
#         gender_dist = GenderDistribution.objects.create(
#             female_count=female_count,
#             male_count=male_count
#         )
#     else:
#         female_count = gender_dist.female_count
#         male_count = gender_dist.male_count
#
#     # الحصول على مقاييس المشاركة
#     engagement = EngagementMetrics.objects.first()
#     if engagement:
#         follow_count = engagement.follow_count
#         comment_count = engagement.comment_count
#         like_count = engagement.like_count
#     else:
#         # إنشاء مقاييس مشاركة افتراضية
#         engagement = EngagementMetrics.objects.create(
#             follow_count=10,
#             comment_count=15,
#             like_count=20
#         )
#         follow_count = 10
#         comment_count = 15
#         like_count = 20
#
#     # الحصول على رؤى لوحة المعلومات
#     insights = DashboardInsights.objects.first()
#     if not insights:
#         # حساب أعلى نشاط للمستخدمين في يوم واحد
#         user_counts = UserActivity.objects.values('date__date').annotate(
#             user_count=Count('user', distinct=True)
#         ).order_by('-user_count')
#
#         highest_active = user_counts.first()
#         highest_active_users = highest_active['user_count'] if highest_active else 0
#
#         # إنشاء رؤى لوحة المعلومات
#         insights = DashboardInsights.objects.create(
#             highest_active_users=highest_active_users,
#             total_accounts=total_accounts,
#             most_used_feature=feature_names[0] if feature_names else "",
#             total_itineraries=0,
#             avg_itineraries_per_user=0.0,
#             avg_journey_duration=0
#         )
#     else:
#         highest_active_users = insights.highest_active_users
#         total_accounts = insights.total_accounts
#         most_used_feature = insights.most_used_feature
#         total_itineraries = insights.total_itineraries
#         avg_itineraries_per_user = insights.avg_itineraries_per_user
#         avg_journey_duration = insights.avg_journey_duration
#
#     data = {
#         'activity_dates': [date.strftime('%Y-%m-%d') for date in activity_dates],
#         'activity_counts': activity_counts,
#         'female_count': female_count,
#         'male_count': male_count,
#         'feature_name': feature_names,
#         'feature_usage': feature_usage_counts,
#         'follow_count': follow_count,
#         'comment_count': comment_count,
#         'like_count': like_count,
#         'highest_active_users': highest_active_users,
#         'total_accounts': total_accounts,
#         'most_used_feature': most_used_feature,
#         'total_itineraries': total_itineraries,
#         'avg_itineraries_per_user': avg_itineraries_per_user,
#         'avg_journey_duration': avg_journey_duration,
#     }
#
#     return render(request, 'analytics.html', data)
from django.db.models import Count
#
# @login_required
# @user_passes_test(is_staff)
# def monitor(request):
#     """عرض صفحة مراقبة المستخدمين وإدارتهم"""
#     # الحصول على جميع المستخدمين مع معلومات ملفاتهم الشخصية
#     users = User.objects.all().order_by('-date_joined')
#
#     # المستخدم المحدد الافتراضي (لا يوجد)
#     selected_user = None
#     selected_user_id = request.GET.get('user_id')
#
#     # إذا تم توفير معرف المستخدم في معلمات الاستعلام، احصل على هذا المستخدم المحدد
#     if selected_user_id:
#         try:
#             selected_user = User.objects.get(id=selected_user_id)
#         except User.DoesNotExist:
#             pass  # احتفظ بالمستخدم المحدد الافتراضي كـ None
#
#     # الحصول على وقت آخر نشاط للمستخدم المحدد
#     last_activity = None
#     if selected_user:
#         last_activity = timezone.now()  # الافتراضي هو الآن
#         user_activity = UserActivity.objects.filter(user=selected_user).order_by('-date').first()
#         if user_activity:
#             last_activity = user_activity.date
#
#     # التحقق من وجود رسائل خطأ أو نجاح
#     messages_list = messages.get_messages(request)
#
#     context = {
#         'users': users,
#         'selected_user': selected_user,
#         'last_activity': last_activity,
#         'messages': messages_list,
#     }
#
#     return render(request, 'monitor.html', context)
#
#
# @login_required
# @user_passes_test(is_staff)
# def edit_user(request):
#     """تعديل تفاصيل المستخدم (اسم المستخدم، البريد الإلكتروني، حالة الإشراف)"""
#     if request.method != 'POST':
#         return redirect('admin_app:monitor')
#
#     user_id = request.POST.get('user_id')
#     user = get_object_or_404(User, id=user_id)
#
#     # لا تسمح للمسؤولين بتعديل حسابات المستخدمين الفائقين ما لم يكونوا مستخدمين فائقين
#     if user.is_superuser and not request.user.is_superuser:
#         messages.error(request, "ليس لديك إذن لتعديل هذا المستخدم.")
#         return redirect('admin_app:monitor')
#
#     # تحديث تفاصيل المستخدم
#     username = request.POST.get('username')
#     email = request.POST.get('email')
#     is_staff = request.POST.get('is_staff') == 'true'
#
#     # التحقق من فرادة اسم المستخدم (إذا تم تغييره)
#     if username != user.username and User.objects.filter(username=username).exists():
#         messages.error(request, f"اسم المستخدم '{username}' مستخدم بالفعل.")
#         return redirect(f'/admin_app/monitor/?user_id={user_id}')
#
#     # التحقق من فرادة البريد الإلكتروني (إذا تم تغييره)
#     if email != user.email and User.objects.filter(email=email).exists():
#         messages.error(request, f"البريد الإلكتروني '{email}' مسجل بالفعل.")
#         return redirect(f'/admin_app/monitor/?user_id={user_id}')
#
#     # حفظ التغييرات
#     user.username = username
#     user.email = email
#
#     # فقط قم بتحديث حالة الإشراف إذا كان المحرر مستخدمًا فائقًا
#     if request.user.is_superuser:
#         user.is_staff = is_staff
#
#     user.save()
#     messages.success(request, f"تم تحديث المستخدم '{username}' بنجاح.")
#     return redirect(f'/admin_app/monitor/?user_id={user_id}')
#
#
# @login_required
# @user_passes_test(is_staff)
# def reset_user_password(request):
#     """إعادة تعيين كلمة مرور المستخدم"""
#     if request.method != 'POST':
#         return redirect('admin_app:monitor')
#
#     user_id = request.POST.get('user_id')
#     user = get_object_or_404(User, id=user_id)
#
#     # لا تسمح للمسؤولين بتغيير كلمات مرور المستخدمين الفائقين ما لم يكونوا مستخدمين فائقين
#     if user.is_superuser and not request.user.is_superuser:
#         messages.error(request, "ليس لديك إذن لإعادة تعيين كلمة مرور هذا المستخدم.")
#         return redirect('admin_app:monitor')
#
#     new_password = request.POST.get('new_password')
#     confirm_password = request.POST.get('confirm_password')
#
#     # التحقق من كلمات المرور
#     if new_password != confirm_password:
#         messages.error(request, "كلمات المرور غير متطابقة.")
#         return redirect(f'/admin_app/monitor/?user_id={user_id}')
#
#     if len(new_password) < 8:
#         messages.error(request, "يجب أن تكون كلمة المرور 8 أحرف على الأقل.")
#         return redirect(f'/admin_app/monitor/?user_id={user_id}')
#
#     # تعيين كلمة المرور الجديدة
#     user.set_password(new_password)
#     user.save()
#
#     messages.success(request, f"تمت إعادة تعيين كلمة مرور '{user.username}'.")
#     return redirect(f'/admin_app/monitor/?user_id={user_id}')
#
#
# @login_required
# @user_passes_test(is_staff)
# def toggle_user_status(request):
#     """تفعيل/تعطيل حساب المستخدم"""
#     if request.method != 'POST':
#         return redirect('admin_app:monitor')
#
#     user_id = request.POST.get('user_id')
#     user = get_object_or_404(User, id=user_id)
#
#     # لا تسمح للمسؤولين بتعطيل حسابات المستخدمين الفائقين ما لم يكونوا مستخدمين فائقين
#     if user.is_superuser and not request.user.is_superuser:
#         messages.error(request, "ليس لديك إذن لتعطيل حساب هذا المستخدم.")
#         return redirect('admin_app:monitor')
#
#     # تبديل حالة النشاط
#     user.is_active = not user.is_active
#     user.save()
#
#     status = "تفعيل" if user.is_active else "تعطيل"
#     messages.success(request, f"تم {status} حساب '{user.username}'.")
#     return redirect(f'/admin_app/monitor/?user_id={user_id}')
#
#
# @login_required
# @user_passes_test(is_staff)
# def delete_user(request):
#     """حذف حساب المستخدم"""
#     if request.method != 'POST':
#         return redirect('admin_app:monitor')
#
#     user_id = request.POST.get('user_id')
#     user = get_object_or_404(User, id=user_id)
#
#     # لا تسمح لأي شخص بحذف حسابات المستخدمين الفائقين إلا لمستخدم فائق آخر
#     if user.is_superuser and not request.user.is_superuser:
#         messages.error(request, "ليس لديك إذن لحذف حساب هذا المستخدم.")
#         return redirect('admin_app:monitor')
#
#     # أيضًا لا تسمح للمستخدمين بحذف حساباتهم الخاصة
#     if user.id == request.user.id:
#         messages.error(request, "لا يمكنك حذف حسابك الخاص.")
#         return redirect('admin_app:monitor')
#
#     username = user.username
#     user.delete()
#
#     messages.success(request, f"تم حذف المستخدم '{username}'.")
#     return redirect('/admin_app/monitor/')


# accounts/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from user_app.models import UserProfile
from .models import Notification, SupportTicket, TicketResponse, Traveler, TravelerNote, TravelerVerification, Trip, \
    Itinerary, FeatureUsage, GenderDistribution, EngagementMetrics, DashboardInsights, UserActivity

from django.views.decorators.http import require_POST

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, POI
from django.contrib import messages

from .utils import get_user_activity


def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def analytics(request):
    """عرض صفحة التحليلات والإحصائيات"""
    # الحصول على بيانات نشاط المستخدمين
    activity_dates, activity_counts = get_user_activity()

    # قيم افتراضية في حالة عدم وجود نماذج
    feature_names = []
    feature_usage_counts = []
    female_count = 0
    male_count = 0
    follow_count = 0
    comment_count = 0
    like_count = 0
    highest_active_users = 0
    total_accounts = User.objects.count()  # على الأقل يمكننا حساب المستخدمين
    most_used_feature = ""
    total_itineraries = 0
    avg_itineraries_per_user = 0
    avg_journey_duration = 0

    # الحصول على بيانات استخدام الميزات
    feature_usages = FeatureUsage.objects.all().order_by('-click_count')[:5]  # أعلى 5 ميزات
    if feature_usages:
        feature_names = [feature.feature_name for feature in feature_usages]
        feature_usage_counts = [feature.click_count for feature in feature_usages]

    # إذا لم توجد بيانات استخدام ميزات، أنشئ بيانات افتراضية
    if not feature_usages:
        default_features = ['Profile', 'Explore', 'Trips', 'Favorites', 'Map']
        for i, feature in enumerate(default_features):
            FeatureUsage.objects.get_or_create(
                feature_name=feature,
                defaults={'click_count': (i + 1) * 2}
            )
        # إعادة جلب البيانات بعد الإنشاء
        feature_usages = FeatureUsage.objects.all().order_by('-click_count')[:5]
        feature_names = [feature.feature_name for feature in feature_usages]
        feature_usage_counts = [feature.click_count for feature in feature_usages]

    # الحصول على توزيع النوع
    gender_dist = GenderDistribution.objects.first()
    if not gender_dist:
        # تحديث إحصاءات النوع من ملفات تعريف المستخدمين
        female_count = UserProfile.objects.filter(gender='F').count()
        male_count = UserProfile.objects.filter(gender='M').count()
        gender_dist = GenderDistribution.objects.create(
            female_count=female_count,
            male_count=male_count
        )
    else:
        female_count = gender_dist.female_count
        male_count = gender_dist.male_count

    # الحصول على مقاييس المشاركة
    engagement = EngagementMetrics.objects.first()
    if engagement:
        follow_count = engagement.follow_count
        comment_count = engagement.comment_count
        like_count = engagement.like_count
    else:
        # إنشاء مقاييس مشاركة افتراضية
        engagement = EngagementMetrics.objects.create(
            follow_count=10,
            comment_count=15,
            like_count=20
        )
        follow_count = 10
        comment_count = 15
        like_count = 20

    # الحصول على رؤى لوحة المعلومات
    insights = DashboardInsights.objects.first()
    if not insights:
        # حساب أعلى نشاط للمستخدمين في يوم واحد
        user_counts = UserActivity.objects.values('date__date').annotate(
            user_count=Count('user', distinct=True)
        ).order_by('-user_count')

        highest_active = user_counts.first()
        highest_active_users = highest_active['user_count'] if highest_active else 0

        # إنشاء رؤى لوحة المعلومات
        insights = DashboardInsights.objects.create(
            highest_active_users=highest_active_users,
            total_accounts=total_accounts,
            most_used_feature=feature_names[0] if feature_names else "",
            total_itineraries=0,
            avg_itineraries_per_user=0.0,
            avg_journey_duration=0
        )
    else:
        highest_active_users = insights.highest_active_users
        total_accounts = insights.total_accounts
        most_used_feature = insights.most_used_feature
        total_itineraries = insights.total_itineraries
        avg_itineraries_per_user = insights.avg_itineraries_per_user
        avg_journey_duration = insights.avg_journey_duration

    data = {
        'activity_dates': [date.strftime('%Y-%m-%d') for date in activity_dates],
        'activity_counts': activity_counts,
        'female_count': female_count,
        'male_count': male_count,
        'feature_name': feature_names,
        'feature_usage': feature_usage_counts,
        'follow_count': follow_count,
        'comment_count': comment_count,
        'like_count': like_count,
        'highest_active_users': highest_active_users,
        'total_accounts': total_accounts,
        'most_used_feature': most_used_feature,
        'total_itineraries': total_itineraries,
        'avg_itineraries_per_user': avg_itineraries_per_user,
        'avg_journey_duration': avg_journey_duration,
    }

    return render(request, 'analytics.html', data)


@login_required
def dashboard(request):
    user = request.user
    # محاولة الحصول على سجل Traveler أو إنشاؤه إذا لم يكن موجوداً
    traveler, created = Traveler.objects.get_or_create(user=user)

    context = {
        'user': user,
        'total_trips': Trip.objects.filter(traveler=traveler).count(),
        'upcoming_trips': Trip.objects.filter(
            traveler=traveler,
            start_date__gte=timezone.now().date()
        ).count(),
        'countries_visited': Itinerary.objects.filter(
            trip__traveler=traveler
        ).values('location').distinct().count(),
        'recent_trips': Trip.objects.filter(
            traveler=traveler
        ).order_by('-start_date')[:5]
    }

    return render(request, 'templates/accounts/dashboard.html', context)


# views.py
@login_required
def my_trips_view(request):
    user = request.user
    traveler = Traveler.objects.get(user=user)

    trips = Trip.objects.filter(traveler=traveler).order_by('-start_date')

    context = {
        'user': user,
        'trips': trips,
    }

    return render(request, 'templates/accounts/my_trips.html', context)


@require_POST
@login_required
def create_trip(request):
    try:
        user = request.user
        traveler = Traveler.objects.get(user=user)

        trip = Trip.objects.create(
            name=request.POST.get('name'),
            traveler=traveler,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            category=request.POST.get('category'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            latitude=float(request.POST.get('latitude')),
            longitude=float(request.POST.get('longitude'))
        )

        return JsonResponse({
            'success': True,
            'trip': {
                'id': trip.id,
                'name': trip.name,
                'start_date': trip.start_date,
                'end_date': trip.end_date,
                'category': trip.category,
                'location': trip.location
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# views.py
@login_required
def map_view(request):
    user = request.user
    traveler = Traveler.objects.get(user=user)
    trips = Trip.objects.filter(traveler=traveler)

    context = {
        'user': user,
        'trips': trips,
    }

    return render(request, 'templates/accounts/map.html', context)


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'templates/accounts/category_list.html', {
        'categories': categories
    })


@login_required
def category_create(request):
    if request.method == 'POST':
        try:
            category = Category.objects.create(
                name=request.POST['name'],
                description=request.POST['description']
            )
            if 'icon' in request.FILES:
                category.icon = request.FILES['icon']
                category.save()
            messages.success(request, 'تم إنشاء الفئة بنجاح')
            return redirect('category_list')
        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
    return render(request, 'templates/accounts/category_form.html')


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        try:
            category.name = request.POST['name']
            category.description = request.POST['description']
            if 'icon' in request.FILES:
                category.icon = request.FILES['icon']
            category.save()
            messages.success(request, 'تم تحديث الفئة بنجاح')
            return redirect('category_list')
        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
    return render(request, 'templates/accounts/category_form.html', {'category': category})


@login_required
def poi_list(request):
    pois = POI.objects.all()
    return render(request, 'templates/accounts/poi_list.html', {
        'pois': pois
    })


@login_required
def poi_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            poi = POI.objects.create(
                name=request.POST['name'],
                category_id=request.POST['category'],
                description=request.POST['description'],
                location=request.POST['location'],
                latitude=float(request.POST['latitude']),
                longitude=float(request.POST['longitude'])
            )
            if 'image' in request.FILES:
                poi.image = request.FILES['image']
                poi.save()
            messages.success(request, 'تم إنشاء نقطة الاهتمام بنجاح')
            return redirect('poi_list')
        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
    return render(request, 'templates/accounts/poi_form.html', {'categories': categories})


@login_required
def poi_edit(request, pk):
    poi = get_object_or_404(POI, pk=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            poi.name = request.POST['name']
            poi.category_id = request.POST['category']
            poi.description = request.POST['description']
            poi.location = request.POST['location']
            poi.latitude = float(request.POST['latitude'])
            poi.longitude = float(request.POST['longitude'])
            if 'image' in request.FILES:
                poi.image = request.FILES['image']
            poi.save()
            messages.success(request, 'تم تحديث نقطة الاهتمام بنجاح')
            return redirect('poi_list')
        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
    return render(request, 'templates/accounts/poi_form.html', {
        'poi': poi,
        'categories': categories
    })


@login_required
def traveler_list(request):
    travelers = Traveler.objects.select_related('user', 'verification').all()
    return render(request, 'templates/accounts/traveler_list.html', {
        'travelers': travelers
    })


@login_required
def traveler_detail(request, pk):
    traveler = get_object_or_404(Traveler.objects.select_related('user', 'verification'), pk=pk)
    support_tickets = traveler.support_tickets.all()
    notes = traveler.admin_notes.all().order_by('-created_at')

    if request.method == 'POST':
        if 'add_note' in request.POST:
            TravelerNote.objects.create(
                traveler=traveler,
                author=request.user,
                note=request.POST['note']
            )
        elif 'verify_traveler' in request.POST:
            verification, created = TravelerVerification.objects.get_or_create(traveler=traveler)
            verification.status = 'verified'
            verification.verified_at = timezone.now()
            verification.verified_by = request.user
            verification.save()

        return redirect('traveler_detail', pk=pk)

    return render(request, 'templates/accounts/traveler_detail.html', {
        'traveler': traveler,
        'support_tickets': support_tickets,
        'notes': notes
    })


@login_required
def support_ticket_list(request):
    tickets = SupportTicket.objects.select_related('traveler__user', 'assigned_to').all()
    return render(request, 'templates/accounts/support_ticket_list.html', {
        'tickets': tickets
    })


@login_required
def support_ticket_detail(request, pk):
    ticket = get_object_or_404(SupportTicket.objects.select_related('traveler__user'), pk=pk)
    responses = ticket.responses.all().order_by('created_at')

    if request.method == 'POST':
        if 'add_response' in request.POST:
            TicketResponse.objects.create(
                ticket=ticket,
                responder=request.user,
                message=request.POST['message'],
                is_staff_response=True
            )
        elif 'update_status' in request.POST:
            ticket.status = request.POST['status']
            ticket.save()
        elif 'assign_ticket' in request.POST:
            ticket.assigned_to = request.user
            ticket.save()

        return redirect('support_ticket_detail', pk=pk)

    staff_users = User.objects.filter(is_staff=True)

    return render(request, 'templates/accounts/support_ticket_detail.html', {
        'ticket': ticket,
        'responses': responses,
        'staff_users': staff_users
    })


@login_required
def support_ticket_list(request):
    tickets = SupportTicket.objects.select_related('traveler__user', 'assigned_to').all()

    context = {
        'tickets': tickets,
        'new_tickets_count': tickets.filter(status='new').count(),
        'in_progress_tickets_count': tickets.filter(status='in_progress').count(),
        'resolved_tickets_count': tickets.filter(status='resolved').count(),
        'urgent_tickets_count': tickets.filter(priority='urgent').count(),
    }

    return render(request, 'templates/accounts/support_ticket_list.html', context)


@login_required
def user_list(request):
    users = User.objects.all().order_by('-date_joined')

    context = {
        'users': users,
        'active_users_count': users.filter(is_active=True).count(),
        'staff_users_count': users.filter(is_staff=True).count(),
        'new_users_count': users.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=30)).count(),
    }

    return render(request, 'templates/accounts/user_list.html', context)


@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        if 'toggle_active' in request.POST:
            user.is_active = not user.is_active
            user.save()
            messages.success(request, f'تم {"تفعيل" if user.is_active else "تعطيل"} المستخدم بنجاح')

        elif 'toggle_staff' in request.POST:
            user.is_staff = not user.is_staff
            user.save()
            messages.success(request, f'تم {"منح" if user.is_staff else "سحب"} صلاحيات الإدارة')

        elif 'reset_password' in request.POST:
            # إنشاء كلمة مرور عشوائية
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.save()
            messages.success(request, f'تم تعيين كلمة المرور الجديدة: {new_password}')

        return redirect('user_detail', pk=pk)

    context = {
        'user_detail': user,
        'last_login': user.last_login,
        'date_joined': user.date_joined,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
    }

    # إذا كان المستخدم مسافر، نضيف معلومات إضافية
    try:
        traveler = user.traveler
        context.update({
            'is_traveler': True,
            'trips_count': traveler.trips.count(),
            'verification_status': traveler.verification.status if hasattr(traveler, 'verification') else None,
        })
    except Traveler.DoesNotExist:
        context['is_traveler'] = False

    return render(request, 'templates/accounts/user_detail.html', context)


@login_required
def user_create(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            is_staff = request.POST.get('is_staff', False)

            # إنشاء المستخدم
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.is_staff = is_staff
            user.save()

            # إنشاء حساب مسافر إذا تم تحديد ذلك
            if request.POST.get('create_traveler', False):
                Traveler.objects.create(user=user)

            messages.success(request, 'تم إنشاء المستخدم بنجاح')
            return redirect('admin:user_list')

        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')

    return render(request, 'templates/accounts/user_form.html')


@staff_member_required
def notification_list(request):
    """عرض قائمة الإشعارات وإدارتها"""
    notifications = Notification.objects.all().order_by('-notification_date')

    context = {
        'notifications': notifications,
        'unread_count': notifications.filter(is_read=False).count(),
        'system_count': notifications.filter(notification_type='system').count(),
        'trip_count': notifications.filter(notification_type='trip').count()
    }

    return render(request, 'templates/accounts/notification_list.html', context)


@staff_member_required
def notification_create(request):
    """إنشاء إشعار جديد"""
    travelers = Traveler.objects.all()

    if request.method == 'POST':
        try:
            notification_type = request.POST.get('notification_type')
            message = request.POST.get('message')
            notification_date = request.POST.get('notification_date', timezone.now())

            # إذا كان الإشعار لمسافر محدد
            if 'traveler_id' in request.POST and request.POST.get('traveler_id'):
                traveler = get_object_or_404(Traveler, id=request.POST.get('traveler_id'))
                notification = Notification.objects.create(
                    traveler=traveler,
                    message=message,
                    notification_type=notification_type,
                    notification_date=notification_date,
                    is_read=False
                )
                messages.success(request, f'تم إنشاء إشعار لـ {traveler.user.username}')

            # إذا كان الإشعار لجميع المسافرين
            elif request.POST.get('send_to_all'):
                for traveler in travelers:
                    Notification.objects.create(
                        traveler=traveler,
                        message=message,
                        notification_type=notification_type,
                        notification_date=notification_date,
                        is_read=False
                    )
                messages.success(request, 'تم إنشاء إشعار لجميع المسافرين')

            return redirect('notification_list')

        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')

    return render(request, 'templates/accounts/notification_form.html', {
        'travelers': travelers
    })


@staff_member_required
def notification_delete(request, pk):
    """حذف إشعار"""
    notification = get_object_or_404(Notification, pk=pk)

    if request.method == 'POST':
        notification.delete()
        messages.success(request, 'تم حذف الإشعار بنجاح')
        return redirect('notification_list')

    return redirect('notification_list')


@login_required
def user_notifications(request):
    """عرض إشعارات المستخدم الحالي"""
    user = request.user
    # استخدام get_or_create بدلاً من get_object_or_404
    traveler, created = Traveler.objects.get_or_create(user=user)
    notifications = Notification.objects.filter(traveler=traveler).order_by('-notification_date')

    context = {
        'notifications': notifications,
        'unread_count': notifications.filter(is_read=False).count()
    }

    return render(request, 'templates/accounts/user_notifications.html', context)


@login_required
def mark_notification_read(request, pk):
    """تحديد إشعار كمقروء"""
    notification = get_object_or_404(Notification, pk=pk)

    # التأكد من أن الإشعار يخص المستخدم الحالي
    traveler, created = Traveler.objects.get_or_create(user=request.user)
    if notification.traveler != traveler:
        messages.error(request, 'لا يمكنك الوصول لهذا الإشعار')
        return redirect('user_notifications')

    notification.is_read = True
    notification.save()

    return redirect('user_notifications')


@login_required
def unread_notifications_count(request):
    """الحصول على عدد الإشعارات غير المقروءة للمستخدم الحالي"""
    user = request.user
    traveler, created = Traveler.objects.get_or_create(user=user)
    count = Notification.objects.filter(traveler=traveler, is_read=False).count()

    return JsonResponse({'count': count})


# API function to get unread notifications count
@login_required
def unread_notifications_count(request):
    """الحصول على عدد الإشعارات غير المقروءة للمستخدم الحالي"""
    user = request.user
    traveler = get_object_or_404(Traveler, user=user)
    count = Notification.objects.filter(traveler=traveler, is_read=False).count()

    return JsonResponse({'count': count})


@require_POST
def ajax_logout(request):
    logout(request)
    return JsonResponse({'success': True})

