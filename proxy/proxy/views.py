from django.shortcuts import render

def proxy(request):
	return render(request, 'templates/output.html', ({}))