from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("dashboard/login/", views.dashboard_login, name="dashboard_login"),
    path("dashboard/logout/", views.dashboard_logout, name="dashboard_logout"),
    path("dashboard/", views.dashboard_home, name="dashboard_home"),
    path("dashboard/projects/", views.dashboard_projects, name="dashboard_projects"),
    path("dashboard/projects/new/", views.project_create, name="project_create"),
    path("dashboard/projects/<int:pk>/edit/", views.project_edit, name="project_edit"),
    path("dashboard/projects/<int:pk>/delete/", views.project_delete, name="project_delete"),
    path("dashboard/appointments/", views.dashboard_appointments, name="dashboard_appointments"),
    path("dashboard/appointments/<int:pk>/toggle/", views.appointment_toggle, name="appointment_toggle"),
    path("dashboard/appointments/<int:pk>/delete/", views.appointment_delete, name="appointment_delete"),
    path("dashboard/appointments/export/", views.appointment_export, name="appointment_export"),
]
