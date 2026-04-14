from django import forms
from .models import Target, TargetUpdate


class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = [
            "title",
            "target_type",
            "system_name",
            "structure_name",
            "objective",
            "priority",
            "status",
            "timer_start",
            "timer_final",
            "notes",
        ]
        widgets = {
            "timer_start": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "timer_final": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

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
