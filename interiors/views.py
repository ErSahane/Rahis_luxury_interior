import csv

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AppointmentForm, ProjectForm
from .models import Appointment, Project, ProjectImage, Service, Testimonial


PHONE_NUMBER = "+919911280073"
WHATSAPP_NUMBER = "919911280073"


def seed_defaults():
    services = [
        ("Modular Kitchen", "modular-kitchen", "fa-solid fa-kitchen-set", "Smart kitchens with premium shutters, quartz tops, storage systems, and luxury finishes."),
        ("Luxury Wardrobe", "luxury-wardrobe", "fa-solid fa-door-closed", "Custom wardrobes and almari units designed for beauty, capacity, and smooth daily use."),
        ("Custom Furniture", "custom-furniture", "fa-solid fa-couch", "Made-to-measure sofas, beds, tables, and storage pieces built around your lifestyle."),
        ("Wooden Interior", "wooden-interior", "fa-solid fa-tree", "Warm wooden wall panels, partitions, ceiling details, and handcrafted interior accents."),
        ("Office Setup", "office-setup", "fa-solid fa-briefcase", "Professional office furniture, cabins, workstations, and storage with a refined finish."),
        ("Sofa & Bed Design", "sofa-bed-design", "fa-solid fa-bed", "Elegant sofa sets, headboards, beds, and lounge furniture tailored to your room."),
        ("Carpenter Services", "carpenter-services", "fa-solid fa-hammer", "Reliable carpenter work for repairs, custom builds, fittings, and polish work."),
        ("Home Renovation", "home-renovation", "fa-solid fa-house-chimney", "Complete renovation planning for modern homes, bedrooms, kitchens, and living spaces."),
    ]
    for index, (title, slug, icon, description) in enumerate(services, start=1):
        Service.objects.get_or_create(
            slug=slug,
            defaults={"title": title, "icon": icon, "description": description, "order": index},
        )

    if not Testimonial.objects.exists():
        Testimonial.objects.create(client_name="Aamir Khan", location="Patna", rating=5, message="The finishing and planning felt truly premium. Our wardrobe and TV panel changed the whole room.")
        Testimonial.objects.create(client_name="Neha Sharma", location="Gaya", rating=5, message="Rahis Luxury Interiors handled our kitchen like professionals. Clean work, beautiful materials, and on-time delivery.")


def home(request):
    seed_defaults()
    appointment_form = AppointmentForm()
    if request.method == "POST":
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment_form.save()
            messages.success(request, "Your appointment request has been sent. We will call you shortly.")
            return redirect("home")

    context = {
        "appointment_form": appointment_form,
        "services": Service.objects.filter(is_featured=True),
        "projects": Project.objects.filter(is_featured=True)[:12],
        "categories": Project.CATEGORY_CHOICES,
        "testimonials": Testimonial.objects.filter(is_active=True)[:8],
        "stats": {"years": 12, "projects": 350, "clients": 290, "finish": 100},
        "phone_number": PHONE_NUMBER,
        "whatsapp_number": WHATSAPP_NUMBER,
    }
    return render(request, "interiors/home.html", context)


def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment booked successfully.")
    return redirect("home")


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard_home")
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect("dashboard_home")
        messages.error(request, "Invalid username or password.")
    return render(request, "dashboard/login.html")


def dashboard_logout(request):
    logout(request)
    return redirect("dashboard_login")


@login_required
def dashboard_home(request):
    context = {
        "total_projects": Project.objects.count(),
        "total_appointments": Appointment.objects.count(),
        "pending_appointments": Appointment.objects.filter(is_completed=False).count(),
        "recent_projects": Project.objects.all()[:5],
        "recent_appointments": Appointment.objects.all()[:6],
    }
    return render(request, "dashboard/home.html", context)


@login_required
def dashboard_projects(request):
    return render(request, "dashboard/projects.html", {"projects": Project.objects.all()})


def save_gallery_images(project, files):
    for image in files:
        ProjectImage.objects.create(project=project, image=image, caption=project.title)


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        project = form.save()
        save_gallery_images(project, request.FILES.getlist("gallery_images"))
        messages.success(request, "Project added successfully.")
        return redirect("dashboard_projects")
    return render(request, "dashboard/project_form.html", {"form": form, "title": "Add New Project"})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if request.method == "POST" and form.is_valid():
        project = form.save()
        save_gallery_images(project, request.FILES.getlist("gallery_images"))
        messages.success(request, "Project updated successfully.")
        return redirect("dashboard_projects")
    return render(request, "dashboard/project_form.html", {"form": form, "project": project, "title": "Edit Project"})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted.")
        return redirect("dashboard_projects")
    return render(request, "dashboard/confirm_delete.html", {"object": project, "cancel_url": "dashboard_projects"})


@login_required
def dashboard_appointments(request):
    return render(request, "dashboard/appointments.html", {"appointments": Appointment.objects.all()})


@login_required
def appointment_toggle(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.is_completed = not appointment.is_completed
    appointment.save(update_fields=["is_completed"])
    return redirect("dashboard_appointments")


@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
        messages.success(request, "Appointment deleted.")
        return redirect("dashboard_appointments")
    return render(request, "dashboard/confirm_delete.html", {"object": appointment, "cancel_url": "dashboard_appointments"})


@login_required
def appointment_export(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="rahis-appointments.csv"'
    writer = csv.writer(response)
    writer.writerow(["Name", "Mobile", "Address", "Work Type", "Preferred Date", "Message", "Completed", "Created"])
    for item in Appointment.objects.all():
        writer.writerow([item.name, item.mobile, item.address, item.get_work_type_display(), item.preferred_date, item.message, item.is_completed, item.created_at])
    return response

# Create your views here.
