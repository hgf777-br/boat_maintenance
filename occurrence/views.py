import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView
from rest_framework import serializers

from boat.models import Boat
from maintenance.models import Maintenance, Sectors

from .forms import CheckInOutForm, CheckOutForm, OccurrenceForm
from .models import CheckInOut, Item, Occurrence


class OccurrencesTableView(LoginRequiredMixin, ListView):
    model = Occurrence
    template_name = "occurrence/table_occurrences.html"
    context_object_name = "occurrences_list"
    success_url = reverse_lazy("occurrence:table-occurrences")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sectors = {sector[0]: sector[1] for sector in Sectors.choices}
        context["sectors"] = sectors
        return context

    def get_queryset(self):
        if self.request.user.profile == 'SO':
            boat_user = self.request.user.get_boat()
            return Occurrence.objects.filter(boat=boat_user)
        return Occurrence.objects.all()


class OccurrenceCreateView(LoginRequiredMixin, CreateView):
    model = Occurrence
    form_class = OccurrenceForm
    template_name = "occurrence/create_occurrence.html"
    success_url = reverse_lazy("occurrence:table-occurrences")

    def form_valid(self, form):
        occurrence = form.save(commit=False)
        occurrence.creator = self.request.user
        occurrence.save()
        messages.success(self.request, 'Ocorrência criada com sucesso')
        return HttpResponseRedirect(self.success_url)


class OccurrenceUpdateView(LoginRequiredMixin, UpdateView):
    model = Occurrence
    form_class = OccurrenceForm
    template_name = "occurrence/update_occurrence.html"
    success_url = reverse_lazy("occurrence:table-occurrences")

    def form_valid(self, form):
        messages.success(self.request, 'Ocorrência atualizada com sucesso')
        return super().form_valid(form)


class OccurrenceDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            occurrence = Occurrence.objects.get(pk=kwargs["pk"])
            occurrence.delete()
            return JsonResponse({"status": "ok", "message": "Ocorrência excluída com sucesso"})
        except ObjectDoesNotExist:
            return JsonResponse({"status": "error", "message": "Ocorrência não encontrada"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


class OccurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occurrence
        fields = '__all__'

    def to_representation(self, instance):
        instance.sector = instance.get_sector_display()
        response = super().to_representation(instance)
        response['boat'] = instance.boat.name
        return response


class OccurrenceCreateMaintenanceView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            boat = Boat.objects.get(name=data['boat'])
            maintenance = Maintenance(
                due_date=data['due_date'],
                sector=data['sector'],
                description=data['description'],
                obs=data['obs'],
                boat=boat,
                creator=request.user
            )
            maintenance.save()
            occurrence = Occurrence.objects.get(pk=data['occurrence_id'])
            occurrence.maintenance = maintenance
            occurrence.save()
            return JsonResponse({"status": "ok", "message": "Manutenção criada com sucesso"})
        except ObjectDoesNotExist:
            return JsonResponse({"status": "error", "message": "Ocorrência ou técnico não encontrados"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})


class CheckInOutsTableView(LoginRequiredMixin, ListView):
    model = CheckInOut
    template_name = "check_in_out/table_check_in_outs.html"
    context_object_name = "check_in_out_list"


class CheckInOutCreateView(LoginRequiredMixin, CreateView):
    model = CheckInOut
    form_class = CheckInOutForm
    template_name = "check_in_out/create_check_in.html"
    success_url = reverse_lazy("occurrence:table-check-in-outs")

    def form_valid(self, form):
        check_in_out = form.save(commit=False)
        check_in_out.creator = self.request.user
        check_in_out.save()
        messages.success(self.request, 'Checkin criado com sucesso')
        return HttpResponseRedirect(self.success_url)


class CheckInOutUpdateView(LoginRequiredMixin, UpdateView):
    model = CheckInOut
    form_class = CheckInOutForm
    template_name = "check_in_out/update_check_in_out.html"
    success_url = reverse_lazy("occurrence:table-check-in-outs")

    def form_valid(self, form):
        messages.success(self.request, 'Checkin atualizado com sucesso')
        return super().form_valid(form)


class CheckInOutDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            check_in_out = CheckInOut.objects.get(pk=kwargs["pk"])
            check_in_out.delete()
            return JsonResponse({"status": "ok", "message": "CheckIn excluído com sucesso"})
        except ObjectDoesNotExist:
            return JsonResponse({"status": "error", "message": "CheckIn não encontrado"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


class CheckInOutCheckoutView(LoginRequiredMixin, UpdateView):
    model = CheckInOut
    form_class = CheckOutForm
    template_name = "check_in_out/check_out.html"
    success_url = reverse_lazy("occurrence:table-check-in-outs")

    def setup(self, request, *args, **kwargs):
        all_items = Item.objects.all().order_by('name')
        self.items = {
            sector[1]: [
                item.name for item in all_items if item.sector == sector[0]
            ] for sector in Sectors.choices
        }
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.items

        return context

    def form_valid(self, form):
        print(self.request.POST)
        messages.success(self.request, 'Checkout realizado com sucesso')
        return super().form_valid(form)
