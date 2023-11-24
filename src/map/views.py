from django.shortcuts import render
from map.forms import SearchForm
from django.http import JsonResponse


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

    form = SearchForm()
    context = {'form': form}

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)

    return render(request, 'index.html', context)
