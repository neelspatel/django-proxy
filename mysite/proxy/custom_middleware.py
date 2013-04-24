import mysite

class custom_middleware(object):
	def process_request(self, request):
		return mysite.views.proxy(request)