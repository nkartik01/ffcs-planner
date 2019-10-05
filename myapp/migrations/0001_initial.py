# Generated by Django 2.2.6 on 2019-10-04 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='course',
            fields=[
                ('course_code', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('course_title', models.CharField(max_length=120)),
                ('l_credits', models.IntegerField()),
                ('t_credits', models.IntegerField()),
                ('p_credits', models.IntegerField()),
                ('j_credits', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='teacher',
            fields=[
                ('name', models.CharField(max_length=120)),
                ('emp_code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('school', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_id', models.CharField(max_length=2)),
                ('slot_name', models.CharField(max_length=5)),
            ],
            options={
                'unique_together': {('slot_name', 'slot_id')},
            },
        ),
        migrations.CreateModel(
            name='offering',
            fields=[
                ('offer_id', models.IntegerField(primary_key=True, serialize=False)),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.course')),
                ('emp_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='offer_set',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.offering')),
                ('slot_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.slot')),
            ],
        ),
    ]