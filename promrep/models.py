from django.db import models

from model_utils.models import TimeStampedModel

class Praenomen(models.Model):
    abbrev = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Praenomina'
        ordering = ['name']


class Sex(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name


class RoleType(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=1024, unique=True)

    def __unicode__(self):
        return self.name


class Person(TimeStampedModel):
    praenomen = models.ForeignKey(Praenomen)
    nomen = models.CharField(max_length=128, unique=True)
    cognomen = models.CharField(max_length=128, unique=True)

    sex = models.ForeignKey(Sex)

    real_number = models.CharField(max_length=32, unique=True)
    real_attribute = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        name_parts = [self.praenomen, self.nomen, self.cognomen]
        return " ".join(name_parts)

class Office(TimeStampedModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, unique=True)
    notes = models.CharField(max_length=1024, unique=True)

    def __unicode__(self):
        return self.name

class AssertionType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Assertion(TimeStampedModel):
    persons = models.ManyToManyField(Person, through='AssertionPerson')
    assertion_type = models.ForeignKey(AssertionType)

    display_text = models.CharField(max_length=1024, unique=True)

    date_year = models.CharField(max_length=64, unique=True)

    notes = models.CharField(max_length=1024, unique=True)



class AssertionPerson(TimeStampedModel):

    person = models.ForeignKey(Person)
    assertion = models.ForeignKey(Assertion)

    role = models.ForeignKey(RoleType)
    original_text = models.CharField(max_length=1024, unique=True)






