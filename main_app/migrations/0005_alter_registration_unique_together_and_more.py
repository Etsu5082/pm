# Generated by Django 5.1.3 on 2024-11-09 08:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_registration_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together=set(),
        ),
        migrations.AddIndex(
            model_name='registration',
            index=models.Index(fields=['user', 'practice'], name='main_app_re_user_id_123db0_idx'),
        ),
        migrations.AddConstraint(
            model_name='registration',
            constraint=models.UniqueConstraint(fields=('user', 'practice'), name='unique_user_practice'),
        ),
    ]