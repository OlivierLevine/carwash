from django.views import generic

from .models import Pos, AvailableService, AvailableFuel


class IndexView(generic.ListView):
    template_name = 'pos/index.html'
    context_object_name = 'latest_pos_list'

    def get_queryset(self):
        list = Pos.objects.order_by('-id')[:50]
        for pos in list:
            pos.services = AvailableService.objects.filter(pos=pos).select_related("service")
            pos.fuels = AvailableFuel.objects.filter(pos=pos).select_related("fuel")
        return list


class DetailView(generic.DetailView):
    model = Pos
    template_name = 'pos/detail.html'
