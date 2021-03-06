# Generated by Django 2.1 on 2018-08-31 05:52

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_bloguser_usericon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bloguser',
            options={'verbose_name_plural': '博客用户表'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': '分类表'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_time'], 'verbose_name_plural': '文章表'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': '文章状态表'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name_plural': '标签表'},
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=DjangoUeditor.models.UEditorField(blank=True, verbose_name='正文'),
        ),
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.CharField(blank=True, help_text='可选，如若为空将摘取正文的前54个字符', max_length=100, null=True, verbose_name='文章摘要'),
        ),
    ]
