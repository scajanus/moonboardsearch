# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class Holds(models.Model):
#     position = models.TextField(db_column='Position', blank=True, null=True)  # Field name made lowercase.
#     setup = models.TextField(db_column='Setup', blank=True, null=True)  # Field name made lowercase.
#     holdset = models.TextField(db_column='HoldSet', blank=True, null=True)  # Field name made lowercase.
#     hold = models.IntegerField(db_column='Hold', blank=True, null=True)  # Field name made lowercase.
#     orientation = models.TextField(db_column='Orientation', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'holds'
#         app_label = 'moonboard'


class ProblemMove(models.Model):
    id = models.AutoField(primary_key=True, default="")
    problem = models.ForeignKey('Problem', models.DO_NOTHING, blank=True, null=True)
    position = models.TextField(blank=True, null=True)
    setup = models.TextField(blank=True, null=True)
    setangle = models.IntegerField(blank=True, null=True)
    isstart = models.IntegerField(blank=True, null=True)
    isend = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        unique_together = ('problem', 'position',)
        # db_table = 'problemMoves'
        # app_label = 'moonboard'


# class Problemmoves2016(models.Model):
#     problem = models.IntegerField(db_column='Problem', blank=True, null=True)  # Field name made lowercase.
#     position = models.TextField(db_column='Position', blank=True, null=True)  # Field name made lowercase.
#     holdset = models.TextField(db_column='HoldSet', blank=True, null=True)  # Field name made lowercase.
#     isstart = models.IntegerField(db_column='IsStart', blank=True, null=True)  # Field name made lowercase.
#     isend = models.IntegerField(db_column='IsEnd', blank=True, null=True)  # Field name made lowercase.

#     class Meta:
#         managed = True
#         db_table = 'problemMoves_2016'
#         app_label = 'moonboard'


class Problem(models.Model):
    id = models.IntegerField(primary_key=True, blank=True, null=False)  # Field name made lowercase.
    name = models.TextField(blank=True, null=True)  # Field name made lowercase.
    grade = models.TextField(blank=True, null=True)  # Field name made lowercase.
    benchmark = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    assessmentproblem = models.IntegerField(blank=True, null=True)  # Field name made lowercase.
    method = models.TextField(blank=True, null=True)  # Field name made lowercase.
    firstname = models.TextField(blank=True, null=True)  # Field name made lowercase.
    lastname = models.TextField(blank=True, null=True)  # Field name made lowercase.
    setyear = models.IntegerField(blank=False, null=False)
    setangle = models.IntegerField(blank=False, null=False)
    repeats = models.IntegerField(blank=False, null=False)
    rating = models.TextField(blank=False, null=False)
    dateinserted = models.TextField(blank=False, null=False)

    class Meta:
        managed = True
        # db_table = 'problems'
        # app_label = 'moonboard'


class Setter(models.Model):
    firstname = models.TextField(blank=True, null=True)  # Field name made lowercase.
    lastname = models.TextField(blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        # db_table = 'setter'
        # app_label = 'moonboard'
