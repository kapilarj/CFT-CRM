from django.db import models
from .models import Task, Time_Entry
from django.views.generic import TemplateView, ListView
from .forms import CreateTaskForm
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from apps.users.models import MyUser
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from apps.project.models import IT_Project
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import redirect
from django.db.models import Sum, ExpressionWrapper, F, fields
import datetime
from django.db.models import Q

class TaskList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Task
    context_object_name = 'task_list'
    permission_required = ('task.view_task', 'users.view_users',)
    template_name = 'task_manager_list.html'

    def get_queryset(self):
        queryset = Task.objects.filter(project__id=self.kwargs.get('pk'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_id'] = self.kwargs.get('pk')

        return context



class Employee_Task_List(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('task.view_task',)
    model = Task
    context_object_name = 'emp_task_list'
    template_name = "my tasks.html"

    def get_queryset(self):
        temp = Task.objects.filter(employee_id=self.request.user)

        return temp


class TaskCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    permission_required = ('task.add_task')
    form_class = CreateTaskForm
    template_name = "create_task_form.html"
    success_url = '/project'

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     print(self.kwargs)
    #     kwargs.update({'project_id': self.kwargs.get('pk')})
    #
    #     return kwargs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['project_id'] = self.kwargs.get('pk')
    #
    #     return context


class Edit_Task(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('task.change_task',)
    form_class = CreateTaskForm
    template_name = "create_task_form.html"
    success_url = '/task'


class Details_Task(LoginRequiredMixin, PermissionRequiredMixin, DetailView,):
    permission_required = ('task.view_task', 'users.view_users',)
    model = Task
    context_object_name = 'task_list'
    template_name = "task_details.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        s=""
        if Time_Entry.objects.filter(task_id=self.kwargs.get('pk')).last() is None:
            s="No time spent"
        else:
            q=Time_Entry.objects.filter(task_id=self.kwargs.get('pk')).last()
            if q.time_spent is not None:
                    # print("ENtered if")
                    s = str(q.time_spent.hour)+ " hrs "+str(q.time_spent.minute)+" min's"
                    # print(s)
        context['time']=s

        return context

class Details_Task_Emp(LoginRequiredMixin, PermissionRequiredMixin, DetailView,):
    permission_required = ('task.view_task',)
    model = Task
    context_object_name = 'task_list'
    template_name = "test.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        s=""
        if Time_Entry.objects.filter(task_id=self.kwargs.get('pk')).last() is None:
            s="No time spent"
        else:
            q=Time_Entry.objects.filter(task_id=self.kwargs.get('pk')).last()
            if q.time_spent is not None:
                    # print("ENtered if")
                    s = str(q.time_spent.hour)+ " hrs "+str(q.time_spent.minute)+" min's"
                    # print(s)
        context['time']=s

        return context

@login_required
@permission_required('task.add_time_entry', raise_exception=True)
def entry(request, pk):

        if not request.user.is_authenticated:
            return HttpResponseForbidden
        # elif Time_Entry.objects.filter(task_start_date_time=datetime.today()):
        #     return HttpResponse("Task Already started! You can start working")
        else:

            tas = Task.objects.get(pk=pk)


            a = Time_Entry.objects.create(task=tas,
                                          task_start_date_time=datetime.datetime.now(),
                                          )
            a.save()
            # print(tas)task:task-detail
            tas.task_current_state = 'running'
            tas.save()
            return redirect(reverse('task:task-details', kwargs={'pk' : tas.id}))

@login_required
@permission_required('task.add_time_entry', raise_exception=True)
def end(request, pk):

        if not request.user.is_authenticated:
            return HttpResponseForbidden
        else:
            tas = Task.objects.get(pk=pk)
            tmp = Time_Entry.objects.filter(task=tas, task_end_date_time=None).order_by('-id').first()
            one = datetime.datetime.now()
            # print(type(one))
            tmp.task_end_date_time = one
            tmp.save()

            #for storing the value of time_per_session
            delta = datetime.timedelta(hours=tmp.task_start_date_time.hour, minutes=tmp.task_start_date_time.minute)
            var = tmp.task_end_date_time-delta
            # print(type(var))
            # print(var)
            s=str(var.hour)+"hrs" + str(var.minute)+" minute"
            #print(s)
            tmp.time_per_session = var
            tmp.save()

            #for storing the value of time spent
            # using last entry of time spent + new time_per_session entry

            if tmp.id == 1:
                tmp.time_spent = tmp.time_per_session
                tmp.save()

            # elif tmp.time_spent is None:
            #     tmp.time_spent = tmp.time_per_session
            #     tmp.save()

            else:
                print("*********************************")
                print(tmp.id)

                new1 = Time_Entry.objects.get(Q(id=(tmp.id-1)) & Q(task=tas))
                #print(new1)
                h=new1.time_spent.hour
                m=new1.time_spent.minute
                time_spent_delta = tmp.time_per_session + datetime.timedelta(hours=h, minutes=m)
                #print(time_spent_delta)
                tmp.time_spent = time_spent_delta
                tmp.save()

            tas.task_current_state = 'stopped'
            tas.save()
            #print(tmp.id)
            return redirect(reverse('task:task-details', kwargs= {'pk' : tas.id}))
