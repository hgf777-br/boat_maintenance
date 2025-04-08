from datetime import datetime, timedelta
import json
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, View, DetailView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.response import Response

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
            maintenance = Maintenance.objects.get(pk=data['maintenance_id'])
            if data['has_schedule']:
                finish_date = datetime.strptime(data['finish_date'], r'%Y-%m-%d')
                maintenance.finish_date = finish_date
                maintenance.engine_hours = int(data['engine_hours']) if data['engine_hours'] else None
                maintenance.value = float(data['value']) if data['value'] else None
                maintenance.completed = True
                if maintenance.periodic:
                    new_maintenance = Maintenance(
                        boat=maintenance.periodic.boat,
                        due_date=maintenance.periodic.new_due_date(base_date=maintenance.due_date),
                        sector=maintenance.periodic.sector,
                        description=maintenance.periodic.description,
                        creator=maintenance.periodic.creator,
                        periodic=maintenance.periodic,
                    )
                    new_maintenance.save()
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


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'
        
    def to_representation(self, instance):
        instance.due_date = instance.due_date.strftime(r'%d/%m/%Y')
        instance.sector = instance.get_sector_display()
        instance.schedule_date = instance.schedule_date.strftime(r'%d/%m/%Y') if instance.schedule_date else 'não agendada'
        instance.finish_date = instance.finish_date.strftime(r'%d/%m/%Y') if instance.finish_date else 'não concluída'
        ret = super().to_representation(instance)
        ret['boat'] = instance.boat.name
        ret['technician'] = instance.technician.name
        print(ret)
        return ret

class MaintenanceDetailsView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        maintenance = Maintenance.objects.get(pk=pk)
        serialized_data = MaintenanceSerializer(maintenance)
        return JsonResponse(serialized_data.data)

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
        due_date = periodic.new_due_date(initial_run=True)
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


class PeriodicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodic
        fields = '__all__'
        
    def to_representation(self, instance):
        instance.sector = instance.get_sector_display()
        instance.periodicity_week_day = instance.get_periodicity_week_day_display()
        instance.periodicity_month = instance.get_periodicity_month_display()
        ret = super().to_representation(instance)
        ret['boat'] = instance.boat.name
        ret['periodicity_display'] = instance.get_periodicity_display()
        print(ret)
        return ret

class PeriodicDetailsView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        periodic = Periodic.objects.get(pk=pk)
        serialized_data = PeriodicSerializer(periodic)
        return JsonResponse(serialized_data.data)