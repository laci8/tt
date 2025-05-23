# Generated by Django 5.2 on 2025-04-15 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_visitor_canvas_fp_visitor_fonts_fp_visitor_webgl_fp_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visitor',
            options={'verbose_name': 'Visitor', 'verbose_name_plural': 'Visitors'},
        ),
        migrations.RenameField(
            model_name='behaviordata',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='pagevisit',
            name='visitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='tracker.visitor'),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='canvas_fp',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='fonts_fp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='webgl_fp',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
