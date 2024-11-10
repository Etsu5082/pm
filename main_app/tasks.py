# main_app/tasks.py
from django.utils import timezone
from datetime import timedelta
from .models import Practice

def close_old_practices():
    target_date = timezone.now().date() + timedelta(days=5)
    practices = Practice.objects.filter(date=target_date, is_closed=False)
    for practice in practices:
        practice.is_closed = True
        practice.save()