from django.conf import settings
from django.db import models


class TargetType(models.TextChoices):
    ASTRAHUS = "ASTRAHUS", "Astrahus"
    FORTIZAR = "FORTIZAR", "Fortizar"
    KEEPSTAR = "KEEPSTAR", "Keepstar"
    RAITARU = "RAITARU", "Raitaru"
    AZBEL = "AZBEL", "Azbel"
    SOTIYO = "SOTIYO", "Sotiyo"
    ATHANOR = "ATHANOR", "Athanor"
    TATARA = "TATARA", "Tatara"
    POCO_SKYHOOK = "POCO_SKYHOOK", "POCO / Skyhook"
    SOVEREIGNTY = "SOVEREIGNTY", "Sovereignty"
    POS = "POS", "POS"
    METENOX = "METENOX", "Metenox"


class Target(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        CANCELED = "CANCELED", "Canceled"

    class Objective(models.TextChoices):
        REINFORCE = "REINFORCE", "Reinforce"
        FINAL = "FINAL", "Final"
        DEFEND = "DEFEND", "Defend"
        OTHER = "OTHER", "Other"

    class TargetType(models.TextChoices):
        ASTRAHUS = "ASTRAHUS", "Astrahus"
        FORTIZAR = "FORTIZAR", "Fortizar"
        KEEPSTAR = "KEEPSTAR", "Keepstar"
        RAITARU = "RAITARU", "Raitaru"
        AZBEL = "AZBEL", "Azbel"
        SOTIYO = "SOTIYO", "Sotiyo"
        ATHANOR = "ATHANOR", "Athanor"
        TATARA = "TATARA", "Tatara"
        POCO_SKYHOOK = "POCO_SKYHOOK", "POCO / Skyhook"
        SOVEREIGNTY = "SOVEREIGNTY", "Sovereignty"
        POS = "POS", "POS"
        METENOX = "METENOX", "Metenox"

    title = models.CharField(max_length=200)

    target_type = models.CharField(
        max_length=20,
        choices=TargetType.choices,
        default=TargetType.ASTRAHUS,
    )

    solar_system = models.ForeignKey(
        "eveuniverse.EveSolarSystem",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="aa_targetboard_targets",
    )

    @property
    def system_name(self) -> str:
        return self.solar_system.name if self.solar_system else ""
    structure_name = models.CharField(max_length=255, blank=True, default="")

    objective = models.CharField(
        max_length=20,
        choices=Objective.choices,
        default=Objective.OTHER,
    )

    priority = models.PositiveSmallIntegerField(default=3)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )

    timer_start = models.DateTimeField(null=True, blank=True)
    timer_final = models.DateTimeField(null=True, blank=True)

    notes = models.TextField(blank=True, default="")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="aa_targetboard_targets_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at", "-created_at")
        default_permissions = ()
        permissions = (
            ("basic_access", "Can access the Target Board"),
            ("manage_targets", "Can add, edit, and delete targets"),
        )

    def __str__(self) -> str:
        return self.title

class TargetUpdate(models.Model):
    target = models.ForeignKey(
        Target,
        on_delete=models.CASCADE,
        related_name="updates",
    )
    body = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="aa_targetboard_target_updates_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Update on {self.target_id} @ {self.created_at:%Y-%m-%d %H:%M}"