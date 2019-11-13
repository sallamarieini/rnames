from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Location, Name, Qualifier, Relation, Reference, StructuredName
from .filters import LocationFilter, NameFilter, QualifierFilter, ReferenceFilter, RelationFilter, StructuredNameFilter
from .forms import LocationForm, NameForm, QualifierForm, ReferenceForm, RelationForm, StructuredNameForm
from django.contrib.auth.models import User
from .filters import UserFilter, APINameFilter


#def name_list(request):
#    names = Name.objects.is_active().order_by('name')
#    names = Name.objects.order_by('name')
#    return render(request, 'rnames_app/name_list.html', {'names': names})

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_names=Name.objects.is_active().count()
    num_opinions=Relation.objects.is_active().count()
    num_references=Reference.objects.is_active().count()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'rnames_app/base_generic.html',
        context={'num_names':num_names,'num_opinions':num_opinions,'num_references':num_references,}, # num_visits appended
    )

class location_delete(DeleteView):
    model = Location
    success_url = reverse_lazy('location-list')

def location_detail(request, pk):
    location = get_object_or_404(Location, pk=pk)
    return render(request, 'rnames_app/location_detail.html', {'location': location})

def location_edit(request, pk):
    location = get_object_or_404(Location, pk=pk)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            location = form.save(commit=False)
            location.modified_by_id = request.user.id
            location.modified_on = timezone.now()
            location.save()
            return redirect('location-detail', pk=location.pk)
    else:
        form = LocationForm(instance=location)
    return render(request, 'rnames_app/location_edit.html', {'form': form})

def location_list(request):
    f = LocationFilter(request.GET, queryset=Location.objects.is_active().order_by('name'))
    return render(request, 'rnames_app/location_list.html', {'filter': f})

def location_new(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.created_by_id = request.user.id
            location.created_on = timezone.now()
            location.save()
            return redirect('location-detail', pk=location.pk)
    else:
        form = LocationForm()
    return render(request, 'rnames_app/location_edit.html', {'form': form})

class name_delete(DeleteView):
    model = Name
    success_url = reverse_lazy('name-list')

def name_detail(request, pk):
    name = get_object_or_404(Name, pk=pk)
    return render(request, 'rnames_app/name_detail.html', {'name': name})

def name_list(request):
    f = NameFilter(request.GET, queryset=Name.objects.is_active().order_by('name'))
#    f = ProductFilter(request.GET, queryset=Product.objects.all())
    return render(request, 'rnames_app/name_list.html', {'filter': f})

def name_new(request):
    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            name = form.save(commit=False)
#            name.created_by_id = request.user.id
#            name.created_at = timezone.now()
            name.save()
            return redirect('name-detail', pk=name.pk)
    else:
        form = NameForm()
    return render(request, 'rnames_app/name_edit.html', {'form': form})

def name_edit(request, pk):
    name = get_object_or_404(Name, pk=pk)
    if request.method == "POST":
        form = NameForm(request.POST, instance=name)
        if form.is_valid():
            name = form.save(commit=False)
#            name.created_by_id = request.user.id
#            name.created_at = timezone.now()
            name.save()
            return redirect('name-detail', pk=name.pk)
    else:
        form = NameForm(instance=name)
    return render(request, 'rnames_app/name_edit.html', {'form': form})

class qualifier_delete(DeleteView):
    model = Qualifier
    success_url = reverse_lazy('qualifier-list')

def qualifier_detail(request, pk):
    qualifier = get_object_or_404(Qualifier, pk=pk)
    return render(request, 'rnames_app/qualifier_detail.html', {'qualifier': qualifier})

def qualifier_list(request):
    f = QualifierFilter(request.GET, queryset=Qualifier.objects.is_active().order_by('qualifier_name'))
    return render(request, 'rnames_app/qualifier_list.html', {'filter': f})

def qualifier_new(request):
    if request.method == "POST":
        form = QualifierForm(request.POST)
        if form.is_valid():
            qualifier = form.save(commit=False)
            qualifier.save()
            return redirect('qualifier-detail', pk=qualifier.pk)
    else:
        form = QualifierForm()
    return render(request, 'rnames_app/qualifier_edit.html', {'form': form})

def qualifier_edit(request, pk):
    qualifier = get_object_or_404(Qualifier, pk=pk)
    if request.method == "POST":
        form = QualifierForm(request.POST, instance=qualifier)
        if form.is_valid():
            qualifier = form.save(commit=False)
            qualifier.save()
            return redirect('qualifier-detail', pk=qualifier.pk)
    else:
        form = QualifierForm(instance=qualifier)
    return render(request, 'rnames_app/qualifier_edit.html', {'form': form})

def reference_detail(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    return render(request, 'rnames_app/reference_detail.html', {'reference': reference})

def reference_edit(request, pk):
    reference = get_object_or_404(Reference, pk=pk)
    if request.method == "POST":
        form = ReferenceForm(request.POST, instance=reference)
        if form.is_valid():
            reference = form.save(commit=False)
#            name.created_by_id = request.user.id
#            name.created_at = timezone.now()
            reference.save()
            return redirect('reference-detail', pk=reference.pk)
    else:
        form = ReferenceForm(instance=reference)
    return render(request, 'rnames_app/reference_edit.html', {'form': form})

def reference_list(request):
    f = ReferenceFilter(request.GET, queryset=Reference.objects.is_active().order_by('title'))
    return render(request, 'rnames_app/reference_list.html', {'filter': f})

def reference_new(request):
    if request.method == "POST":
        form = ReferenceForm(request.POST)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.save()
            return redirect('reference-detail', pk=reference.pk)
    else:
        form = ReferenceForm()
    return render(request, 'rnames_app/reference_edit.html', {'form': form})

class relation_delete(DeleteView):
    model = Relation
    success_url = reverse_lazy('relation-list')

def relation_detail(request, pk):
    relation = get_object_or_404(Relation, pk=pk)
    return render(request, 'rnames_app/relation_detail.html', {'relation': relation})

def relation_edit(request, pk):
    relation = get_object_or_404(Relation, pk=pk)
    if request.method == "POST":
        form = RelationForm(request.POST, instance=relation)
        if form.is_valid():
            relation = form.save(commit=False)
            relation.save()
            return redirect('relation-detail', pk=relation.pk)
    else:
        form = RelationForm(instance=relation)
    return render(request, 'rnames_app/relation_edit.html', {'form': form})

def relation_list(request):
    f = RelationFilter(request.GET, queryset=Relation.objects.is_active().order_by('name_one'))
    return render(request, 'rnames_app/relation_list.html', {'filter': f})

def relation_new(request):
    if request.method == "POST":
        form = RelationForm(request.POST)
        if form.is_valid():
            relation = form.save(commit=False)
            relation.save()
            return redirect('relation-detail', pk=relation.pk)
    else:
        form = RelationForm()
    return render(request, 'rnames_app/relation_edit.html', {'form': form})

def rnames_detail(request):
    return render(request, 'rnames_app/rnames_detail.html', )

class structuredname_delete(DeleteView):
    model = StructuredName
    success_url = reverse_lazy('structuredname-list')

def structuredname_detail(request, pk):
    structuredname = get_object_or_404(StructuredName, pk=pk)
    return render(request, 'rnames_app/structuredname_detail.html', {'structuredname': structuredname})

def structuredname_list(request):
    f = StructuredNameFilter(request.GET, queryset=StructuredName.objects.is_active().order_by('name', 'qualifier', 'location'))
    return render(request, 'rnames_app/structuredname_list.html', {'filter': f})

def structuredname_new(request):
    if request.method == "POST":
        form = StructuredNameForm(request.POST)
        if form.is_valid():
            structuredname = form.save(commit=False)
            structuredname.save()
            return redirect('structuredname-detail', pk=structuredname.pk)
    else:
        form = StructuredNameForm()
    return render(request, 'rnames_app/structuredname_edit.html', {'form': form})

def structuredname_edit(request, pk):
    structuredname = get_object_or_404(StructuredName, pk=pk)
    if request.method == "POST":
        form = StructuredNameForm(request.POST, instance=structuredname)
        if form.is_valid():
            structuredname = form.save(commit=False)
            structuredname.save()
            return redirect('structuredname-detail', pk=structuredname.pk)
    else:
        form = StructuredNameForm(instance=structuredname)
    return render(request, 'rnames_app/structuredname_edit.html', {'form': form})

def user_search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'rnames_app/user_list.html', {'filter': user_filter})
