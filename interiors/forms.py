from django import forms

from .models import Appointment, Project, ProjectImage, Service, Testimonial


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["work_type"].widget.attrs["class"] = "form-select"

    class Meta:
        model = Appointment
        fields = ["name", "mobile", "address", "work_type", "preferred_date", "message"]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 4}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["category"].widget.attrs["class"] = "form-select"
        self.fields["is_featured"].widget.attrs["class"] = "form-check-input"

    class Meta:
        model = Project
        fields = ["title", "category", "description", "cover_image", "video", "is_featured"]


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ["image", "caption"]


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title", "slug", "description", "icon", "image", "is_featured", "order"]


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["client_name", "location", "rating", "message", "image", "is_active"]
