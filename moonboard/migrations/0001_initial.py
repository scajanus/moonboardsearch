# Generated by Django 3.0.1 on 2020-01-02 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('grade', models.TextField(blank=True, null=True)),
                ('benchmark', models.IntegerField(blank=True, null=True)),
                ('assessmentproblem', models.IntegerField(blank=True, null=True)),
                ('method', models.TextField(blank=True, null=True)),
                ('firstname', models.TextField(blank=True, null=True)),
                ('lastname', models.TextField(blank=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Setter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.TextField(blank=True, null=True)),
                ('lastname', models.TextField(blank=True, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProblemMove',
            fields=[
                ('id', models.AutoField(default='', primary_key=True, serialize=False)),
                ('position', models.TextField(blank=True, null=True)),
                ('setup', models.TextField(blank=True, null=True)),
                ('isstart', models.IntegerField(blank=True, null=True)),
                ('isend', models.IntegerField(blank=True, null=True)),
                ('problem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='moonboard.Problem')),
            ],
            options={
                'managed': True,
            },
        ),
    ]
