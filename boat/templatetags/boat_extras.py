from django import template
from boat.models import Boat

register = template.Library()


def boat_from_user(value, kind='id'):
    boats = Boat.objects.all()
    for boat in boats:
        if (boat.share_owner_1 == value
                or boat.share_owner_2 == value
                or boat.share_owner_3 == value
                or boat.share_owner_4 == value
                or boat.share_owner_5 == value
                or boat.share_owner_6 == value
                or boat.share_owner_7 == value
                or boat.share_owner_8 == value):
            return boat.id if kind == 'id' else boat.name
    return None


def not_in_list(value, list):
    list = list.split(',')
    return value not in list


def technician_full_name(technician):
    if technician:
        return f"{technician.name} - {technician.company}"
    return ""


def dict_value(dict, key):
    return dict.get(key, "")


register.filter("dict_value", dict_value)
register.filter("boat", boat_from_user)
register.filter("not_in_list", not_in_list)
register.filter("technician_full_name", technician_full_name)
