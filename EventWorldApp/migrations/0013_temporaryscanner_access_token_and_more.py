# Generated by Django 5.1.7 on 2025-05-18 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EventWorldApp', '0012_evenement_temp_user_limit_temporaryscanner_can_sell_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='temporaryscanner',
            name='access_token',
            field=models.UUIDField(blank=True, editable=False, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='temporaryscanner',
            name='display_name',
            field=models.CharField(default='Utilisateur_Temporaire', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryscanner',
            name='email',
            field=models.EmailField(default='temporaire@eventworld.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='temporaryscanner',
            name='first_access_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='temporaryscanner',
            name='last_seen_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='temporaryscanner',
            name='can_sell',
            field=models.BooleanField(default=False),
        ),
    ]
