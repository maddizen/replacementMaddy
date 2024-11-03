from django.shortcuts import render, redirect, get_object_or_404
from .models import ProjectQuotation, ProjectElement, Material, ProjectMaterial
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def request_quote(request):
    if request.method == "POST":
        area_size = request.POST.get('area_size')
        description = request.POST.get('description')
        location = request.POST.get('location')
        elements = request.POST.getlist('elements')

        # Create the project quotation
        project = ProjectQuotation.objects.create(
            user=request.user,
            area_size=area_size,
            description=description,
            location=location
        )

        # Loop through selected elements and their materials
        for element_id in elements:
            element = ProjectElement.objects.get(id=element_id)
            materials = request.POST.getlist(f'materials_{element_id}')
            for material_id in materials:
                material = Material.objects.get(id=material_id)
                quantity = request.POST.get(f'quantity_{material_id}')
                if quantity:  # Ensure quantity is provided
                    ProjectMaterial.objects.create(
                        project=project,
                        material=material,
                        quantity=float(quantity)  # Convert to float
                    )

        messages.success(request, "Quotation requested successfully!")
        return redirect('home')

    elements = ProjectElement.objects.all()
    materials = Material.objects.all()
    return render(request, 'quotes/request_quote.html', {'elements': elements, 'materials': materials})

@login_required
def home(request):
    # Get all quotations for the logged-in user
    quotations = ProjectQuotation.objects.filter(user=request.user)
    return render(request, 'quotes/home.html', {'quotations': quotations})

@login_required
def quotation_detail(request, id):
    # Get the specific quotation by ID
    quotation = get_object_or_404(ProjectQuotation, id=id)
    materials = quotation.projectmaterial_set.all()  # Get all materials associated with the quotation
    return render(request, 'quotes/quotation_detail.html', {'quotation': quotation, 'materials': materials})