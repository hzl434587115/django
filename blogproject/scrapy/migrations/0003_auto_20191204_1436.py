# Generated by Django 2.0 on 2019-12-04 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrapy', '0002_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scrapy',
            options={'verbose_name': '网站', 'verbose_name_plural': '网站'},
        ),
        migrations.AddField(
            model_name='category',
            name='pageReplace',
            field=models.CharField(default='', max_length=20, verbose_name='页码'),
        ),
        migrations.AlterField(
            model_name='category',
            name='scrapy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scrapy.Scrapy', verbose_name='网站'),
        ),
    ]
