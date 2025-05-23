import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView

from maintenance.models import Sectors
from occurrence.models import Item
from user.models import User

from .forms import BoatForm
from .models import Boat


class BoatsTableView(LoginRequiredMixin, ListView):
    model = Boat
    template_name = "boat/table_boats.html"
    context_object_name = "boats_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = json.dumps([{'id': user.id, 'name': f'{user.first_name} {user.last_name}'}
                            for user in User.objects.filter(profile='SO')])
        context["users"] = users
        return context


class BoatCreateView(LoginRequiredMixin, CreateView):
    model = Boat
    template_name = "boat/create_boat.html"
    form_class = BoatForm
    success_url = reverse_lazy("boat:table-boats")

    def __init__(self, **kwargs):
        all_items = Item.objects.all().order_by('name')
        self.items = {
            sector[1]: [
                item.name for item in all_items if item.sector == sector[0]
            ] for sector in Sectors.choices
        }

        return super().__init__(**kwargs)

    def form_valid(self, form):
        boat = form.save()
        items_to_add = []
        item_to_remove = []
        for sector, items in self.items.items():
            for idx, item in enumerate(items):
                item_object = Item.objects.get(name=item)
                if self.request.POST.get(f'{sector}-item-{idx}', 'off') == 'on':
                    items_to_add.append(item_object.pk)
                else:
                    item_to_remove.append(item_object.pk)
        boat.items.add(*items_to_add)
        messages.success(self.request, 'Barco criado com sucesso')

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.items

        return context


class BoatUpdateView(LoginRequiredMixin, UpdateView):
    model = Boat
    form_class = BoatForm
    template_name = "boat/update_boat.html"
    success_url = reverse_lazy("boat:table-boats")

    def setup(self, request, *args, **kwargs):
        all_items = Item.objects.all().order_by('name')
        self.items = {
            sector[1]: [
                item.name for item in all_items if item.sector == sector[0]
            ] for sector in Sectors.choices
        }
        self.users_for_notification = []

        return super().setup(request, *args, **kwargs)

    def form_valid(self, form):
        # managing checkout items
        items_to_add = []
        item_to_remove = []
        for sector, items in self.items.items():
            for idx, item in enumerate(items):
                item_object = Item.objects.get(name=item)
                if self.request.POST.get(f'{sector}-item-{idx}', 'off') == 'on':
                    items_to_add.append(item_object.pk)
                else:
                    item_to_remove.append(item_object.pk)
        self.object.items.remove(*item_to_remove)
        self.object.items.add(*items_to_add)

        # managing user to receive reminders
        users_for_notification = [owner for owner in self.object.get_owners() if owner is not None]
        users_for_notification.extend(list(User.objects.exclude(profile='SO')))
        users_to_remove = []
        users_to_add = []
        for idx, user in enumerate(users_for_notification):
            if self.request.POST.get(f'user-{idx}', 'off') == 'on':
                users_to_add.append(user.pk)
            else:
                users_to_remove.append(user.pk)
        self.object.users_notification.remove(*users_to_remove)
        self.object.users_notification.add(*users_to_add)

        messages.success(self.request, 'Barco atualizado com sucesso')

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["boat_items"] = self.object.items.all().values_list('name', flat=True)
        context["boat_users_notification"] = self.object.users_notification.all().values_list('username', flat=True)
        context["items"] = self.items
        users_for_notification = [owner for owner in self.object.get_owners() if owner is not None]
        users_for_notification.extend(list(User.objects.exclude(profile='SO')))
        context['users_for_notification'] = users_for_notification

        return context


class BoatDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            boat = Boat.objects.get(pk=kwargs['pk'])
            boat.delete()
            return JsonResponse({'status': 'ok', 'message': 'Barco excluído com sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Barco não encontrado'})
        except IntegrityError:
            return JsonResponse(
                {'status': 'error', 'message': 'Este barco possui ações em andamento. Exclusão não permitida'}
            )
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


class BoatDetailsListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        boats = {boat.id: {"number_shares": boat.number_shares, "share_owners": boat.get_owners(id=True)}
                 for boat in Boat.objects.all()}
        return JsonResponse(boats)


class BoatUpdateOwnersView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            boat = Boat.objects.get(pk=data['boat_id'])
            boat.set_owners(data['owners'])
            return JsonResponse({'status': 'ok', 'message': 'Proprietários alterados com sucesso'})
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Barco não encontrado'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
