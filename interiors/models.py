from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Service(TimeStampedModel):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=60, default="fa-solid fa-couch")
    image = models.ImageField(upload_to="services/", blank=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Project(TimeStampedModel):
    CATEGORY_CHOICES = [
        ("kitchen", "Kitchen"),
        ("almari", "Almari"),
        ("bedroom", "Bedroom"),
        ("office", "Office"),
        ("luxury", "Luxury Design"),
        ("carpenter", "Carpenter Work"),
    ]

    title = models.CharField(max_length=160)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    description = models.TextField()
    cover_image = models.ImageField(upload_to="projects/")
    video = models.FileField(upload_to="project_videos/", blank=True)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=160, blank=True)

    def __str__(self):
        return f"{self.project.title} image"


class Appointment(TimeStampedModel):
    WORK_TYPES = [
        ("modular_kitchen", "Modular Kitchen"),
        ("wardrobe", "Wardrobe / Almari"),
        ("sofa_bed", "Sofa & Bed Design"),
        ("tv_panel", "TV Panel"),
        ("bedroom", "Bedroom Interior"),
        ("office", "Office Furniture"),
        ("wooden_work", "Wooden Work"),
        ("false_ceiling", "False Ceiling"),
        ("custom", "Custom Carpenter Work"),
    ]

    name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    work_type = models.CharField(max_length=40, choices=WORK_TYPES)
    preferred_date = models.DateField()
    message = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["is_completed", "-created_at"]

    def __str__(self):
        return f"{self.name} - {self.get_work_type_display()}"


class Testimonial(TimeStampedModel):
    client_name = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    message = models.TextField()
    image = models.ImageField(upload_to="testimonials/", blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.client_name

# Create your models here.
