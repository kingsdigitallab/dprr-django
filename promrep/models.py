from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None,
            max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([],
        ["^promrep\.models\.IntegerRangeField"])


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

    description = models.CharField(max_length=1024, blank=True)

    def __unicode__(self):
        return self.name


class Person(TimeStampedModel):
    praenomen = models.ForeignKey(Praenomen)
    nomen = models.CharField(max_length=128)
    cognomen = models.CharField(max_length=128)
    sex = models.ForeignKey(Sex)

    notes = models.CharField(max_length=1024, blank=True)

    filliation = models.CharField(max_length=256, blank=True)

    real_number = models.CharField(max_length=32)
    real_attribute = models.CharField(max_length=128, blank=True)

    def real_id(self):
        r_id = " ".join( [self.real_number, self.real_attribute] )

        return r_id.strip()

    def __unicode__(self):
        name_parts = [self.praenomen, self.nomen, self.cognomen]

        return " ".join(name_parts + self.real_id())


class Office(MPTTModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name


class AssertionType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


class Assertion(TimeStampedModel):
    persons = models.ManyToManyField(Person, through='AssertionPerson')
    assertion_type = models.ForeignKey(AssertionType)

    display_text = models.CharField(max_length=1024, blank=True)
    date_year = models.CharField(max_length=64, blank=True)

    notes = models.CharField(max_length=1024, blank=True)



class AssertionPerson(TimeStampedModel):

    person = models.ForeignKey(Person)
    assertion = models.ForeignKey(Assertion)

    role = models.ForeignKey(RoleType)
    original_text = models.CharField(max_length=1024)


class DateType(models.Model):
    name = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True,
            editable=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)


class Date(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    date_type = models.ForeignKey(DateType, blank=True, null=True)
    interval = models.SmallIntegerField(choices=settings.DATE_INTERVAL_CHOICES)
    year = IntegerRangeField(min_value=-500, max_value=500, blank=True,
                             null=True)
    year_uncertain = models.BooleanField(verbose_name='uncertain')
    month = IntegerRangeField(min_value=1, max_value=12, blank=True, null=True)
    month_uncertain = models.BooleanField(verbose_name='uncertain')
    day = IntegerRangeField(min_value=1, max_value=31, blank=True, null=True)
    day_uncertain = models.BooleanField(verbose_name='uncertain')
    circa = models.BooleanField()
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True,
            editable=False)

    def __unicode__(self):
        return u'%s %s-%s-%s'.strip() % (self.date_type or '', self.year,
                self.month, self.day)






