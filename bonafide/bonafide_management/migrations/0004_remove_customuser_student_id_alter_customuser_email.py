# Generated by Django 4.2.7 on 2023-12-04 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonafide_management', '0003_rename_name_student_registration_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='student_id',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
