from django_cron import CronJobBase, Schedule
from .models import Practice
from django.utils import timezone
from datetime import timedelta

class ClosePracticesCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # 1時間ごとに実行

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'main_app.close_practices_cron_job'  # 一意のコード

    def do(self):
        target_date = timezone.now().date() + timedelta(days=5)
        practices = Practice.objects.filter(date=target_date, is_closed=False)
        for practice in practices:
            practice.is_closed = True
            practice.save()
