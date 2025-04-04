import json
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from user.models import User
from .models import Boat
from .forms import BoatForm

class BoatsTableView(LoginRequiredMixin, ListView):
    model = Boat
    template_name = "boat/table_boats.html"
    context_object_name = "boats_list"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = json.dumps([{'id': user.id, 'name': f'{user.first_name} {user.last_name}'} for user in User.objects.filter(profile='SO')])
        context["users"] = users
        return context


class BoatCreateView(LoginRequiredMixin, CreateView):
    model = Boat
    template_name = "boat/create_boat.html"
    form_class = BoatForm
    success_url = reverse_lazy("boat:table-boats")
    
    def form_valid(self, form):
        messages.success(self.request, 'Barco criado com sucesso')
        return super().form_valid(form)


class BoatUpdateView(LoginRequiredMixin,UpdateView):
    model = Boat
    form_class = BoatForm
    template_name = "boat/update_boat.html"
    success_url = reverse_lazy("boat:table-boats")
    
    def form_valid(self, form):
        messages.success(self.request, 'Barco atualizado com sucesso')
        return super().form_valid(form)
    
    
class BoatDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            boat = Boat.objects.get(pk=kwargs['pk'])
            boat.delete()
            return JsonResponse({'status': 'ok','message': 'Barco excluído com sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error','message': 'Barco não encontrado'})
        except IntegrityError:
            return JsonResponse({'status': 'error','message': 'Este barco possui ações em andamento. Exclusão não permitida'})
        except Exception as e:
            return JsonResponse({'status': 'error','message': str(e)})


class BoatDetailsListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        boats = {boat.id: {"number_shares": boat.number_shares, "share_owners":boat.get_owners(id=True)} for boat in Boat.objects.all()}
        return JsonResponse(boats)

class BoatUpdateOwnersView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            boat = Boat.objects.get(pk=data['boat_id'])
            boat.set_owners(data['owners'])
            return JsonResponse({'status': 'ok','message': 'Proprietários alterados com sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error','message': 'Barco não encontrado'})
        except Exception as e:
            return JsonResponse({'status': 'error','message': str(e)})