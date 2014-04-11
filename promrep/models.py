from django.db import models

from model_utils.models import TimeStampedModel

class Praenomen(models.Model):
    abbrev = models.CharField(max_length=32, unique=True)
    male_form = models.CharField(max_length=128, unique=True)
    female_name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.abbrev


class Sex(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __unicode__(self):
        return self.name


class Gens(TimeStampedModel):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Person(TimeStampedModel):
    praenomen = models.ForeignKey(Praenomen)
    nomen = models.CharField(max_length=128, unique=True)
    cognomen = models.CharField(max_length=128, unique=True)

    sex = models.ForeignKey(Sex)
    gens = models.ForeignKey(Gens)

    real_number = models.CharField(max_length=32, unique=True)

    real_attribute = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        name_parts = [self.praenomen, self.nomen, self.cognomen]
        return " ".join(name_parts)




