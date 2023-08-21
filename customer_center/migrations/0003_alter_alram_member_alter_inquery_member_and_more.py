# Generated by Django 4.2.4 on 2023-08-21 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_alter_member_member_role_alter_member_member_status'),
        ('customer_center', '0002_alter_alram_options_alter_inquery_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alram',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.member'),
        ),
        migrations.AlterField(
            model_name='inquery',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.member'),
        ),
        migrations.AlterField(
            model_name='inqueryresponse',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.member'),
        ),
        migrations.AlterField(
            model_name='inqueryresponse',
            name='inquery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_center.inquery'),
        ),
    ]
