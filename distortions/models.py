from django.db import models

"""
The models in this class are a Python interface to SQL tables in a database.
The tables are created by running the following steps:
- REQUIRED:
  python manage.py makemigrations distortions (creates a Python file in the migrations directory which outlines the series of steps required for the database to match the models)
- OPTIONAL (shows the SQL generated from the new migration):
  python manage.py sqlmigrate distortions <migrationnumber>, where
<migrationnumber> is the number from the file of the most recent migration
created by makemigrations, e.g. '0001' from 0001_initial.py
- OPTIONAL (to ensure the migration won't break anything):
  python manage.py check
- REQUIRED:
  python manage.py migrate (actually applies the migration to the database)
"""


class DistortionType(models.Model):
    # This will be converted into SQL that adds a text field to the
    # table in the database (the distortions_distortiontype table by default)
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class CaughtDistortion(models.Model):
    # This means that when you catch yourself practising distorted thinking,
    # you log a distortion that actually exists
    distortion_type = models.ForeignKey(DistortionType, on_delete=models.CASCADE)
    # This will be used to create a field in the database
    # for storing a date and a time
    caught_at = models.DateTimeField('caught myself at')

    def __str__(self):
        return "%s at %s" % (self.distortion_type.name, self.caught_at)
