from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("aa_targetboard", "0003_alter_target_objective"),
        ("eveuniverse", "__first__"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="target",
            name="system_name",
        ),
        migrations.AddField(
            model_name="target",
            name="solar_system",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="aa_targetboard_targets",
                to="eveuniverse.evesolarSystem",
            ),
        ),
    ]
