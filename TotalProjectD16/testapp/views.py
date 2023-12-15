from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


@permission_required('polls_and_choise', raise_exception=True)
@login_required
def my_view(request):
    return HttpResponse(content={'count': count_var})


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'