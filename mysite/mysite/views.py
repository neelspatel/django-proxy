from django.shortcuts import render

def proxy(request):
	return render(request, 'mysite/output.html', ({}))