# Generated by Django 3.2.4 on 2021-07-20 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_front', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'The Product', 'verbose_name_plural': 'All the Products'},
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(default='S', max_length=2, verbose_name='size'),
        ),
    ]
