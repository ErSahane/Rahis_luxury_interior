from django.contrib import admin

from .models import Appointment, Project, ProjectImage, Service, Testimonial


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_featured", "created_at")
    list_filter = ("category", "is_featured")
    search_fields = ("title", "description")
    inlines = [ProjectImageInline]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "mobile", "work_type", "preferred_date", "is_completed")
    list_filter = ("work_type", "is_completed", "preferred_date")
    search_fields = ("name", "mobile", "address")
    actions = ["mark_completed"]

    @admin.action(description="Mark selected appointments completed")
    def mark_completed(self, request, queryset):
        queryset.update(is_completed=True)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_featured")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "rating", "is_active")

# Register your models here.
