import views
class custom_middleware(object):
	def process_request(self, request):		
		return views.proxy(request)