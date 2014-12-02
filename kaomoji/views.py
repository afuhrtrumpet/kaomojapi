from models import Emoticon
from django.http import HttpResponse

def random(request):
    return HttpResponse(Emoticon.objects.order_by('?')[0].content)
