from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("aa_targetboard", "0004_target_solar_system"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="target",
            options={
                "ordering": ("-updated_at", "-created_at"),
                "default_permissions": (),
                "permissions": (
                    ("basic_access", "Can access the Target Board"),
                    ("manage_targets", "Can add, edit, and delete targets"),
                ),
            },
        ),
    ]
