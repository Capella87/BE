# Generated by Django 3.1 on 2022-02-10 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contest', '0001_initial'),
        ('competition', '0001_initial'),
        ('classes', '0001_initial'),
        ('problem', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('score', models.FloatField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.TextField()),
                ('on_leaderboard', models.BooleanField()),
                ('c_p_id', models.ForeignKey(db_column='c_p_id', on_delete=django.db.models.deletion.CASCADE, to='contest.contest_problem')),
                ('class_id', models.ForeignKey(db_column='class_id', on_delete=django.db.models.deletion.CASCADE, to='classes.class')),
                ('competition_id', models.ForeignKey(db_column='competition_id', on_delete=django.db.models.deletion.CASCADE, to='competition.competition')),
                ('problem_id', models.ForeignKey(db_column='problem_id', on_delete=django.db.models.deletion.CASCADE, to='problem.problem')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
