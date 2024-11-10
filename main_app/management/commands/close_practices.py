# main_app/management/commands/close_practices.py
from django.core.management.base import BaseCommand
from main_app.tasks import close_old_practices

class Command(BaseCommand):
    help = '期限切れの練習を自動的に締め切ります'

    def handle(self, *args, **kwargs):
        close_old_practices()
        self.stdout.write(self.style.SUCCESS('練習の締切処理が完了しました'))