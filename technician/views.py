from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import ProtectedError

from boat_maintenance.mixins import UserNotShareOwner

from .forms import TechnicianForm
from .models import Technician


class TechniciansTableView(UserNotShareOwner, ListView):
    model = Technician
    template_name = "technician/table_technicians.html"
    context_object_name = "technicians_list"


class TechnicianCreateView(UserNotShareOwner, CreateView):
    model = Technician
    template_name = "technician/create_technician.html"
    form_class = TechnicianForm
    success_url = reverse_lazy("technician:table-technicians")

    def form_valid(self, form):
        messages.success(self.request, 'Técnico criado com sucesso')
        return super().form_valid(form)


class TechnicianUpdateView(UserNotShareOwner, UpdateView):
    model = Technician
    form_class = TechnicianForm
    template_name = "technician/update_technician.html"
    success_url = reverse_lazy("technician:table-technicians")

    def form_valid(self, form):
        messages.success(self.request, 'Técnico atualizado com sucesso')
        return super().form_valid(form)


class TechnicianDeleteView(UserNotShareOwner, View):
    def get(self, request, *args, **kwargs):
        try:
            technician = Technician.objects.get(pk=kwargs['pk'])
            technician.delete()
            return JsonResponse({'status': 'ok', 'message': 'Técnico excluído com sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Técnico não encontrado'})
        except ProtectedError:
            return JsonResponse({'status': 'error', 'message': 'Este técnico possui ações no sistema '
                                 'e não pode ser excluído'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
