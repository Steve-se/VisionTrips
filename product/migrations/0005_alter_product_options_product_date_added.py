# Generated by Django 5.0 on 2024-01-06 14:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_name_alter_subcategory_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-date_added'], 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 1, 6, 14, 18, 49, 731602, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
