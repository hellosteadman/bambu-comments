from django.template.response import TemplateResponse
from testproject.myapp.models import Item

def home(request):
    return TemplateResponse(request,
        'home.html',
        Item.objects.all()
    )