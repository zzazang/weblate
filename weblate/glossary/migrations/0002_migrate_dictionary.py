# Generated by Django 3.0.6 on 2020-06-09 09:21

from django.db import migrations


def migrate_dictionary(apps, schema_editor):
    Dictionary = apps.get_model("trans", "Dictionary")
    Project = apps.get_model("trans", "Project")
    Glossary = apps.get_model("glossary", "Glossary")
    Term = apps.get_model("glossary", "Term")
    db_alias = schema_editor.connection.alias

    # Create glossaries for all projects
    glossaries = {
        project.pk: Glossary.objects.create(
            name=project.name, color="silver", project=project
        )
        for project in Project.objects.using(db_alias).iterator()
    }

    # Migrate dictionary to terms
    for dictionary in Dictionary.objects.using(db_alias).iterator():
        # Create new term
        term = Term.objects.create(
            glossary=glossaries[dictionary.project_id],
            language=dictionary.language,
            source=dictionary.source,
            target=dictionary.target,
        )

        # Adjust change links to terms
        dictionary.change_set.update(glossary_term=term)


class Migration(migrations.Migration):

    dependencies = [
        ("glossary", "0001_initial"),
        ("trans", "0085_change_glossary_term"),
    ]

    operations = [
        migrations.RunPython(
            migrate_dictionary, migrations.RunPython.noop, elidable=True
        )
    ]
