import json
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import User
from .forms import UserCreateForm, UserUpdateForm
from boat_maintenance.mixins import UserNotShareOwner

class UsersTableView(UserNotShareOwner, ListView):
    model = User
    template_name = "user/table_users.html"
    context_object_name = "users_list"


class UserCreateView(UserNotShareOwner, CreateView):
    model = User
    template_name = "user/create_user.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("user:table-users")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data["password"])
        user.save()
        messages.success(self.request, "Usuário criado com sucesso")
        return HttpResponseRedirect(self.success_url)


class UserUpdateView(UserNotShareOwner,UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "user/update_user.html"
    success_url = reverse_lazy("user:table-users")
    
    def form_valid(self, form):
        next_page = self.request.POST.get("next", "/")
        form.save()
        messages.success(self.request, "Usuário atualizado com sucesso")
        return redirect(next_page)
    
    
class UserDeleteView(UserNotShareOwner, View):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs["pk"])
            if user.is_superuser:
                raise Exception("Não é possível excluir um superusuário")
            user.delete()
            return JsonResponse({"status": "ok","message": "Usuário excluído com sucesso"})
        except ObjectDoesNotExist:
            return JsonResponse({"status": "error","message": "Usuário não encontrado"})
        except Exception as e:
            return JsonResponse({"status": "error","message": str(e)})


class UserChangePasswordView(UserNotShareOwner, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = User.objects.get(pk=data["user_id"])
        if user.check_password(data["actual_password"]):
            user.set_password(data["new_password"])
            user.save()
            return JsonResponse({"status": "ok", "message": "Senha alterada com sucesso"})
        return JsonResponse({"status": "error", "message": "Senha atual inválida"})


class UserSendNewPasswordView(UserNotShareOwner, View):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs["pk"])
            user.send_new_password_email(request)
            return JsonResponse({"status": "ok", "message": "Senha enviada com sucesso"})
        except ObjectDoesNotExist:
            return JsonResponse({"status": "error","message": "Usuário não encontrado"})
        except Exception as e:
            print(e)
            return JsonResponse({"status": "error", "message": str(e)})