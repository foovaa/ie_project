from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Employees
from django.db.models import Q
from .forms import EmployeeCreateForm, FilterForm, UpdateEmployee, FindForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# API
from rest_framework import generics, permissions, viewsets
from django.views.decorators.csrf import csrf_exempt
from .serializers import EmployeesSerializer



# Create your views here.

@login_required
def index(request):
    return render(request, 'blog/index.html', {})

@login_required
def createEmployee(request):
    my_form = EmployeeCreateForm(request.POST or None)
    if my_form.is_valid():
        my_form.save()
        messages.success(request, 'New Employee added')
        return redirect('/employees')
    context = {
        'form': my_form
    }
    return render(request, 'blog/addEmployee.html', context)

@login_required
def find(request):
    my_form = FindForm(request.POST)
    if my_form.is_valid():
        if 'update' in request.POST:
            return redirect('blog:updateEmployee', p_id=my_form.cleaned_data['personal_id'])
        elif 'delete' in request.POST:
            return redirect('blog:destroy', p_id=my_form.cleaned_data['personal_id'])
    context = {
        'form': my_form
    }
    return render(request, 'blog/find.html', context)




@login_required
def updateEmployee(request, p_id):
    try:
        employee = Employees.objects.get(personal_id=p_id)
        my_form = UpdateEmployee(request.POST or None, instance=employee)
        if my_form.is_valid():
            my_form.save()
            messages.success(request, 'Employee\'s profile updated')
            return redirect('/employees')
    except ObjectDoesNotExist:
        messages.warning(request, 'Enter correct personal id')
        return redirect('/find')
    context = {
        'form': my_form
    }
    # if request.POST:
    return render(request, 'blog/updateEmployee.html', context)


@login_required
def employees(request):
    my_form = FilterForm(request.POST or None)
    if my_form.is_valid():
        emps = Employees.objects.filter((Q(name=my_form.cleaned_data['name']) |
                                         Q(age=my_form.cleaned_data['age'])) |
                                         Q(is_married=my_form.cleaned_data['is_married']))
        return render(request, 'blog/employees_list.html', {'form': my_form, 'employees': emps})
    emps = Employees.objects.all().order_by('-created_at')
    return render(request, 'blog/employees_list.html', {'form': my_form, 'employees': emps})





@login_required
def report(request):
    all_employees = Employees.objects.all().count()
    married_employees = Employees.objects.filter(is_married=True).count()
    not_married_employees = all_employees - married_employees
    salary_bigger_than_10000 = Employees.objects.filter(salary__gte=10000).count()
    top_emp = Employees.objects.all().order_by('-salary')[0]
    lowest_emp = Employees.objects.all().order_by('salary')[0]
    context = {
        'all': all_employees,
        'married': married_employees,
        'not_married': not_married_employees,
        'bigger_than_10000': salary_bigger_than_10000,
        'top': top_emp,
        'lowest': lowest_emp,
    }
    return render(request, 'blog/report.html', context)


@login_required
def destroy(request, p_id):
    try:
        emp = Employees.objects.get(personal_id=p_id)
        emp.delete()
        messages.success(request, 'Employee deleted.')
        return redirect('blog:find')
    except ObjectDoesNotExist:
        messages.warning(request, 'Enter Correct Personal id.')
        return redirect('blog:find')


@login_required
@csrf_exempt
def employees_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        employees = Employees.objects.all()
        serializer = EmployeesSerializer(employees, many=True)
        return JsonResponse(serializer.data, safe=False)




@login_required
@csrf_exempt
def list_by_name(request, name):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        employee = Employees.objects.filter(name=name)
        serializer = EmployeesSerializer(employee, many=True)
        return JsonResponse(serializer.data, safe=False)




@login_required
@csrf_exempt
def update_salary(request, p_id, value):
    """
        Retrieve, update or delete a code snippet.
    """
    try:
        employee = Employees.objects.get(personal_id=p_id)
    except employee.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        employee.salary = value
        employee.save()
        serializer = EmployeesSerializer(employee)
        return JsonResponse(serializer.data)



@login_required
@csrf_exempt
def delete_by_gender(request, gender):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        employees = Employees.objects.filter(gender=gender)
    except employees.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'DELETE':
        employees.delete()
        return HttpResponse(status=204)































