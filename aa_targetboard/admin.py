from django.contrib import admin
from .models import Target, TargetUpdate


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "system_name",
        "target_type",
        "objective",
        "priority",
        "status",
        "timer_final",
        "created_by",
        "created_at",
    )
    list_filter = ("status", "target_type", "priority")
    search_fields = ("title", "system_name", "structure_name", "objective", "notes")


@admin.register(TargetUpdate)
class TargetUpdateAdmin(admin.ModelAdmin):
    list_display = ("target", "created_by", "created_at")
    search_fields = ("body", "target__title", "created_by__username")
    list_filter = ("created_at",)