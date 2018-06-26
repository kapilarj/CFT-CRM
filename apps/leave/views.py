from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import CreateleaveForm
from ..attendance.models import Attendance, LeaveRequest
from .models import Leave
from django.http import HttpResponseForbidden, HttpResponse
from ..users.models import MyUser
from django.db.models import Q
import datetime


class LeaveCreation(CreateView):
    form_class = CreateleaveForm
    template_name = 'assignleave.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return redirect('/')


class LeaveApproval(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('attendance.view_leaverequest',)
    template_name = 'leaves.html'
    model = LeaveRequest
    context_object_name = 'myuser'

    def get_queryset(self):
        queryset = LeaveRequest.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        attend = Attendance.objects.filter(date=datetime.date.today()-datetime.timedelta(days=1), status='absent')
        context['attend'] = attend
        return context


class ShowRequest(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('attendance.view_leaverequest',)
    template_name = 'showrequest.html'
    model = LeaveRequest
    context_object_name = 'leave'

    def get_queryset(self):
        queryset = LeaveRequest.objects.get(id=self.kwargs.get('id'))
        return queryset


class Approve(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('attendance.change_leaverequest',)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden

        else:
            a = LeaveRequest.objects.get(id=self.kwargs.get('id'))
            if a.status == "Pending":
                a.status = "Approved"
                key = a.user_id
                sdate = a.date
                ltype = a.leave_type
                edate = a.end_date
                delta = datetime.timedelta(days=1)
                while sdate <= edate:
                    l = Leave.objects.get(user_id=key)
                    if ltype == "PL":
                        l.pl = l.pl-1
                    elif ltype == "CL":
                        l.cl = l.cl -1
                    else:
                        l.half_day = l.half_day-1
                    l.save()
                    sdate=sdate+delta
                a.save()
                return redirect('/leave/leaverequest')
            else:
                return HttpResponse("Already Approved or Rejected")


class Reject(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('attendance.change_leaverequest',)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden

        else:
            a = LeaveRequest.objects.get(id=self.kwargs.get('id'))
            if a.status == "Pending":
                a.status = "Rejected"
                a.save()
                return redirect('/leave/leaverequest')
            else:
                return HttpResponse("Already Approved or Rejected")


