# Generated by Django 2.2.5 on 2020-01-23 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_auto_20191104_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sidebar',
            name='display_type',
            field=models.PositiveIntegerField(choices=[(1, 'HTML'), (2, '最新文章'), (3, '最热文章'), (4, '最近评论'), (5, '博主介绍')], default=1, verbose_name='展示类型'),
        ),
    ]