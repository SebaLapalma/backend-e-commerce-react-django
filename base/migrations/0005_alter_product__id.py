# Generated by Django 4.1.6 on 2023-02-28 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_product__id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='_id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]