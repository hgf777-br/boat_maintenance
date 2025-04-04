from datetime import datetime, timedelta
import json
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import ObjectDoesNotExist

from .models import Maintenance, Periodic
from .forms import MaintenanceForm, PeriodicForm
from technician.models import Technician

MONTHS = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}

WEEKDAYS = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}


class MaintenancesPendingTableView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = "maintenance/table_pending_maintenances.html"
    context_object_name = "maintenances_list"
    success_url = reverse_lazy("maintenance:table-pending-maintenances")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        technicians = json.dumps([{'id': technician.id, 'name': technician.name} for technician in Technician.objects.all()])
        context["technicians"] = technicians
        return context
    
    def get_queryset(self):
        if self.request.user.profile == 'SO':
            boat_user = self.request.user.get_boat()
            return Maintenance.objects.filter(boat=boat_user, completed=False)
        return Maintenance.objects.filter(completed=False)


class MaintenancesFinishedTableView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = "maintenance/table_finished_maintenances.html"
    context_object_name = "maintenances_list"
    success_url = reverse_lazy("maintenance:table-finished-maintenances")
    
    def get_queryset(self):
        if self.request.user.profile == 'SO':
            boat_user = self.request.user.get_boat()
            return Maintenance.objects.filter(boat=boat_user, completed=True)
        return Maintenance.objects.filter(completed=True)


class MaintenanceCreateView(LoginRequiredMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = "maintenance/create_maintenance.html"
    success_url = reverse_lazy("maintenance:table-pending-maintenances")
    
    def form_valid(self, form):
        maintenance = form.save(commit=False)
        maintenance.creator = self.request.user
        maintenance.save()
        messages.success(self.request, 'Manutenção criada com sucesso')
        return HttpResponseRedirect(self.success_url)


class MaintenanceUpdateView(LoginRequiredMixin, UpdateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = "maintenance/update_maintenance.html"
    success_url = reverse_lazy("maintenance:table-pending-maintenances")
    
    def form_valid(self, form):
        messages.success(self.request, 'Manutenção atualizada com sucesso')
        return super().form_valid(form)


class MaintenanceDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        print('delete')
        try:
            maintenance = Maintenance.objects.get(pk=kwargs['pk'])
            maintenance.delete()
            return JsonResponse({'status': 'ok','message': 'Manutenção excluída com sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error','message': 'Manutenção não encontrada'})
        except Exception as e:
            return JsonResponse({'status': 'error','message': str(e)})


class MaintenanceFlowView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            print(data)
            maintenance = Maintenance.objects.get(pk=data['maintenance_id'])
            if data['has_schedule']:
                finish_date = datetime.strptime(data['finish_date'], r'%Y-%m-%d')
                maintenance.finish_date = finish_date
                maintenance.engine_hours = int(data['engine_hours']) if data['engine_hours'] else None
                maintenance.value = float(data['value']) if data['value'] else None
                maintenance.completed = True
            else:
                schedule_date = datetime.strptime(data['schedule_date'], r'%Y-%m-%d')
                technician = Technician.objects.get(pk=data['technician_id'])
                maintenance.schedule_date = schedule_date
                maintenance.technician = technician
            maintenance.save()
            return JsonResponse({'status': 'ok','message': 'Status da manutenção alterado com sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error','message': 'Manutenção ou técnico não encontrados'})
        except Exception as e:
            return JsonResponse({'status': 'error','message': str(e)})
        

class PeriodicsTableView(LoginRequiredMixin, ListView):
    model=Periodic
    template_name="maintenance/table_periodics.html"
    context_object_name="periodics_list"
    success_url = reverse_lazy("maintenance:table-periodics")
    
    def get_queryset(self):
        if self.request.user.profile == 'SO':
            boat_user = self.request.user.get_boat()
            return Periodic.objects.filter(boat=boat_user)
        return Periodic.objects.all()


class PeriodicCreateView(LoginRequiredMixin, CreateView):
    model=Periodic
    form_class=PeriodicForm
    template_name="maintenance/create_periodic.html"
    success_url = reverse_lazy("maintenance:table-periodics")
    
    def form_valid(self, form):
        periodic = form.save(commit=False)
        periodic.creator = self.request.user
        periodic.save()
        today = datetime.today()
        month = today.month
        year = today.year
        match periodic.periodicity:
            case 'MO':
                if today.day >= periodic.periodicity_day:
                    month = month + 1 if month < 12 else 1
                due_date = datetime(year, month, periodic.periodicity_day)
            case 'WE'|'BW':
                weekday_number = periodic.periodicity_week_day - 1
                if today.weekday() >= weekday_number:
                    day_difference = 7 - abs(today.weekday() - weekday_number)
                    due_date = today + timedelta(days=day_difference)
                else:
                    day_difference = periodic.periodicity_week_day - today.weekday() - 1
                    due_date = today + timedelta(days=day_difference)
                if periodic.periodicity == 'BW':
                    due_date += timedelta(days=7)
            case 'QU'|'SA'|'AN':
                    if month >= periodic.periodicity_month:
                        year += 1
                    due_date = datetime(year, periodic.periodicity_month, periodic.periodicity_day)
            
        maintenance = Maintenance(
            boat=periodic.boat,
            due_date=due_date,
            sector=periodic.sector,
            description=periodic.description,
            creator=periodic.creator,
            periodic=periodic,
        )
        maintenance.save()
        messages.success(self.request, 'Manutenção Periódica criada com sucesso')
        return HttpResponseRedirect(self.success_url)


class PeriodicUpdateView(LoginRequiredMixin, UpdateView):
    model=Periodic
    form_class=PeriodicForm
    template_name="maintenance/update_periodic.html"
    success_url = reverse_lazy("maintenance:table-periodics")
    
    def form_valid(self, form):
        messages.success(self.request, 'Manutenção Periódica atualizada com sucesso')
        return super().form_valid(form)


class PeriodicDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            periodic = Periodic.objects.get(pk=kwargs["pk"])
            periodic.delete()
            return JsonResponse({"status": "ok","message": "Manutenção Periódica excluída com sucesso"})
        except ObjectDoesNotExist:
            return JsonResponse({"status": "error","message": "Manutenção Periódica não encontrada"})
        except Exception as e:
            return JsonResponse({"status": "error","message": str(e)})

