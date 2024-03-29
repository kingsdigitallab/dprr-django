# Generated by Django 3.2 on 2021-09-28 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("promrep", "0079_auto_20171116_1049"),
    ]

    operations = [
        migrations.AlterField(
            model_name="office",
            name="level",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="office",
            name="lft",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="office",
            name="rght",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="person",
            name="nobilis",
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="novus",
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="novus_uncertain",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="person",
            name="patrician",
            field=models.BooleanField(
                default=None, null=True, verbose_name="Patrician"
            ),
        ),
        migrations.AlterField(
            model_name="postassertion",
            name="person",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="post_assertions",
                to="promrep.person",
            ),
        ),
        migrations.AlterField(
            model_name="primarysourcereference",
            name="content_type",
            field=models.ForeignKey(
                blank=True,
                limit_choices_to=models.Q(
                    models.Q(("app_label", "promrep"), ("model", "PersonNote")),
                    models.Q(("app_label", "promrep"), ("model", "PostAssertionNote")),
                    models.Q(
                        ("app_label", "promrep"),
                        ("model", "RelationshipAssertionReference"),
                    ),
                    _connector="OR",
                ),
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="contenttypes.contenttype",
                verbose_name="primary source reference",
            ),
        ),
        migrations.AlterField(
            model_name="primarysourcereference",
            name="primary_source",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="promrep.primarysource",
            ),
        ),
        migrations.AlterField(
            model_name="province",
            name="level",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="province",
            name="lft",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="province",
            name="rght",
            field=models.PositiveIntegerField(editable=False),
        ),
    ]
