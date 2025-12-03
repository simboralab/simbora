from django.shortcuts import render

# Create your views here.
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    return render(request, 'global/page/main.html')