from django.shortcuts import render

from .models import MyModel


def my_view(request):
    model = MyModel()
    model.foo = request.GET.get('foo', '')
    model.save()
    models = MyModel.objects.all()
    return render(request, 'db.html', {'models': models})
