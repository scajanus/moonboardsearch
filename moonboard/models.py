# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Grade(models.Model):
    description = models.CharField(db_column='Description', max_length=3, blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField(db_column='Active', blank=True, null=True)  # Field name made lowercase.
    vgrade = models.CharField(db_column='VGrade', max_length=3, blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    assessmentonly = models.IntegerField(db_column='AssessmentOnly', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    apiid = models.IntegerField(db_column='ApiId', blank=True, null=True)  # Field name made lowercase.
    dateinserted = models.BigIntegerField(db_column='DateInserted', blank=True, null=True)  # Field name made lowercase.
    dateupdated = models.BigIntegerField(db_column='DateUpdated', blank=True, null=True)  # Field name made lowercase.
    datedeleted = models.BigIntegerField(db_column='DateDeleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Grade'


class Hold(models.Model):
    number = models.CharField(db_column='Number', blank=True, null=True, max_length=10)  # Field name made lowercase.
    holdtype = models.IntegerField(db_column='HoldType', blank=True, null=True)  # Field name made lowercase.
    holdsetid = models.IntegerField(db_column='HoldsetId', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    apiid = models.IntegerField(db_column='ApiId', blank=True, null=True)  # Field name made lowercase.
    dateinserted = models.BigIntegerField(db_column='DateInserted', blank=True, null=True)  # Field name made lowercase.
    dateupdated = models.BigIntegerField(db_column='DateUpdated', blank=True, null=True)  # Field name made lowercase.
    datedeleted = models.BigIntegerField(db_column='DateDeleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Hold'


class Holdset(models.Model):
    description = models.CharField(db_column='Description', max_length=150, blank=True, null=True)  # Field name made lowercase.
    color = models.CharField(db_column='Color', blank=True, null=True, max_length=255)  # Field name made lowercase.
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    apiid = models.IntegerField(db_column='ApiId', blank=True, null=True)  # Field name made lowercase.
    dateinserted = models.BigIntegerField(db_column='DateInserted', blank=True, null=True)  # Field name made lowercase.
    dateupdated = models.BigIntegerField(db_column='DateUpdated', blank=True, null=True)  # Field name made lowercase.
    datedeleted = models.BigIntegerField(db_column='DateDeleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HoldSet'


class Holdsetup(models.Model):
    description = models.CharField(db_column='Description', max_length=150)  # Field name made lowercase.
    image = models.CharField(db_column='Image', max_length=50)  # Field name made lowercase.
    holdlayoutid = models.IntegerField(db_column='HoldLayoutId', blank=True, null=True)  # Field name made lowercase.
    allowclimbmethods = models.IntegerField(db_column='AllowClimbMethods', blank=True, null=True)  # Field name made lowercase.
    ismini = models.IntegerField(db_column='IsMini', blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    apiid = models.IntegerField(db_column='ApiId', blank=True, null=True)  # Field name made lowercase.
    dateinserted = models.BigIntegerField(db_column='DateInserted', blank=True, null=True)  # Field name made lowercase.
    dateupdated = models.BigIntegerField(db_column='DateUpdated', blank=True, null=True)  # Field name made lowercase.
    datedeleted = models.BigIntegerField(db_column='DateDeleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HoldSetup'


class Holdsettoholdsetup(models.Model):
    holdsetupid = models.IntegerField(db_column='HoldSetupId')  # Field name made lowercase.
    holdsetid = models.IntegerField(db_column='HoldSetId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HoldsetToHoldSetup'



class Moonboardconfiguration(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=150, blank=True, null=True)  # Field name made lowercase.
    lowgrade = models.CharField(db_column='LowGrade', max_length=3, blank=True, null=True)  # Field name made lowercase.
    highgrade = models.CharField(db_column='HighGrade', max_length=3, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MoonBoardConfiguration'


class Moonboardconfigurationholdsetups(models.Model):
    moonboardconfigurationid = models.IntegerField(db_column='MoonBoardConfigurationId', blank=True, null=True)  # Field name made lowercase.
    holdsetupid = models.IntegerField(db_column='HoldSetupId', blank=True, null=True)  # Field name made lowercase.
    lastproblemid = models.IntegerField(db_column='LastProblemId', blank=True, null=True)  # Field name made lowercase.
    problemlastinserted = models.CharField(db_column='ProblemLastInserted', blank=True, null=True, max_length=255)  # Field name made lowercase.
    problemlastupdated = models.CharField(db_column='ProblemLastUpdated', blank=True, null=True, max_length=255)  # Field name made lowercase.
    problemlastdeleted = models.CharField(db_column='ProblemLastDeleted', blank=True, null=True, max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MoonBoardConfigurationHoldSetups'


class Move(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    problem = models.ForeignKey('Problem', models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(db_column='Description', max_length=10, blank=True, null=True)  # Field name made lowercase.
    isstart = models.IntegerField(db_column='IsStart')  # Field name made lowercase.
    isend = models.IntegerField(db_column='IsEnd')  # Field name made lowercase.
    active = models.IntegerField(db_column='Active', blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order')  # Field name made lowercase.
    apiid = models.IntegerField(db_column='ApiId', blank=True, null=True)  # Field name made lowercase.
    dateinserted = models.BigIntegerField(db_column='DateInserted', blank=True, null=True)  # Field name made lowercase.
    dateupdated = models.BigIntegerField(db_column='DateUpdated', blank=True, null=True)  # Field name made lowercase.
    datedeleted = models.BigIntegerField(db_column='DateDeleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Move'



class Problem(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100, blank=True, null=True)  # Field name made lowercase.
    setupid = models.IntegerField(db_column='SetupId')  # Field name made lowercase.
    moonboardconfigurationid = models.IntegerField(db_column='MoonBoardConfigurationId', blank=True, null=True)  # Field name made lowercase.
    grade = models.CharField(db_column='Grade', max_length=10, blank=True, null=True)  # Field name made lowercase.
    usergrade = models.CharField(db_column='UserGrade', max_length=10, blank=True, null=True)  # Field name made lowercase.
    setby = models.CharField(db_column='Setby', max_length=100, blank=True, null=True)  # Field name made lowercase.
    setbyid = models.CharField(db_column='SetbyId', max_length=128, blank=True, null=True)  # Field name made lowercase.
    holdsets = models.CharField(db_column='Holdsets', max_length=35, blank=True, null=True)  # Field name made lowercase.
    firstascent = models.CharField(db_column='FirstAscent', max_length=100, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='Comment', max_length=100, blank=True, null=True)  # Field name made lowercase.
    method = models.CharField(db_column='Method', max_length=35, blank=True, null=True)  # Field name made lowercase.
    userrating = models.IntegerField(db_column='UserRating', blank=True, null=True)  # Field name made lowercase.
    active = models.IntegerField(db_column='Active', blank=True, null=True)  # Field name made lowercase.
    hasbetavideo = models.IntegerField(db_column='HasBetaVideo', blank=True, null=True)  # Field name made lowercase.
    repeats = models.IntegerField(db_column='Repeats', blank=True, null=True)  # Field name made lowercase.
    moonid = models.IntegerField(db_column='MoonId', blank=True, null=True)  # Field name made lowercase.
    isbenchmark = models.IntegerField(db_column='IsBenchmark', blank=True, null=True)  # Field name made lowercase.
    ismaster = models.IntegerField(db_column='IsMaster', blank=True, null=True)  # Field name made lowercase.
    upgraded = models.IntegerField(db_column='Upgraded', blank=True, null=True)  # Field name made lowercase.
    downgraded = models.IntegerField(db_column='Downgraded', blank=True, null=True)  # Field name made lowercase.
    apiid = models.IntegerField(db_column='ApiId', blank=True, null=True)  # Field name made lowercase.
    dateinserted = models.BigIntegerField(db_column='DateInserted', blank=True, null=True)  # Field name made lowercase.
    dateupdated = models.BigIntegerField(db_column='DateUpdated', blank=True, null=True)  # Field name made lowercase.
    datedeleted = models.BigIntegerField(db_column='DateDeleted', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Problem'



class Problemtoholdset(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    holdsetid = models.IntegerField(db_column='HoldsetId', blank=True, null=True)  # Field name made lowercase.
    problemid = models.IntegerField(db_column='ProblemId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProblemToHoldSet'
