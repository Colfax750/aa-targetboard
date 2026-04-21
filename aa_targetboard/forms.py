from django import forms
from eveuniverse.models import EveSolarSystem
from .models import Target, TargetUpdate


class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = [
            "title",
            "target_type",
            "solar_system",
            "structure_name",
            "objective",
            "priority",
            "status",
            "notes",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
            "solar_system": forms.Select(attrs={
                "class": "select2-solar-system",
                "data-placeholder": "Search for a solar system...",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Select2 AJAX — start with empty queryset unless editing an existing target
        if self.instance and self.instance.pk and self.instance.solar_system_id:
            self.fields["solar_system"].queryset = EveSolarSystem.objects.filter(
                pk=self.instance.solar_system_id
            )
        else:
            self.fields["solar_system"].queryset = EveSolarSystem.objects.none()

        # On POST, include the submitted solar system so Django validation passes
        if self.data and self.data.get("solar_system"):
            try:
                submitted_pk = int(self.data["solar_system"])
                self.fields["solar_system"].queryset = EveSolarSystem.objects.filter(
                    pk=submitted_pk
                )
            except (ValueError, TypeError):
                pass

    def clean_priority(self):
        p = self.cleaned_data["priority"]
        if p < 1 or p > 5:
            raise forms.ValidationError("Priority must be between 1 and 5.")
        return p


class TargetUpdateForm(forms.ModelForm):
    class Meta:
        model = TargetUpdate
        fields = ["body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 3})}
