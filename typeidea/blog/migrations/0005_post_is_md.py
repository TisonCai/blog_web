# Generated by Django 3.0.4 on 2020-03-10 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_post_content_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_md',
            field=models.BooleanField(default=False, verbose_name='使用markdown语法'),
        ),
    ]
