# Generated by Django 5.0.1 on 2024-04-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Telecaller', '0005_leads_assignto_tc_allocate_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='waste_leads',
            name='head_reason',
            field=models.TextField(default=''),
        ),
    ]