from django.shortcuts import render, redirect, get_object_or_404
from .models import ProjectQuotation, ProjectElement, Material, ProjectMaterial
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    pending_projects = ProjectQuotation.objects.filter(status='pending')
    approved_projects = ProjectQuotation.objects.filter(status='approved')
    declined_projects = ProjectQuotation.objects.filter(status='declined')
    completed_projects = ProjectQuotation.objects.filter(status='completed')
    return render(request, 'admin/dashboard.html', {
        'pending_projects': pending_projects,
        'approved_projects': approved_projects,
        'declined_projects': declined_projects,
        'completed_projects': completed_projects,
    })

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(ProjectQuotation, id=project_id)
    elements = ProjectElement.objects.all()
    materials = Material.objects.all()

    if request.method == "POST":
        # Handle updates to project elements, materials, and markup
        # Update logic goes here

        return redirect('admin_dashboard')  # Redirect after processing

    return render(request, 'admin/project_detail.html', {
        'project': project,
        'elements': elements,
        'materials': materials,
    })