# Generated by Django 2.2.5 on 2021-01-16 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_account_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('kakao', 'Kakao'), ('naver', 'Naver'), ('google', 'Google'), ('normal', 'Normal')], max_length=8, null=True),
        ),
    ]
