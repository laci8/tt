# Generated by Django 5.2 on 2025-04-15 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_remove_visitor_asn_remove_visitor_fonts_fp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='fonts_fp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='timezone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='webrtc_support',
            field=models.BooleanField(default=False),
        ),
    ]
