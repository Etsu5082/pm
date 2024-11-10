# main_app/management/commands/close_registrations.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from main_app.models import Practice

class Command(BaseCommand):
    help = '練習日4日前の0:00に参加申請を締め切る'

    def handle(self, *args, **kwargs):
        target_date = (timezone.now() + timedelta(days=4)).date()
        # 練習日の4日前の0:00に閉鎖するため、当日の練習を対象とする
        practices_to_close = Practice.objects.filter(date__date=target_date, is_closed=False)
        count = practices_to_close.update(is_closed=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully closed {count} registrations for practices on {target_date}'))
