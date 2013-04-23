from django.shortcuts import render

import httplib2
import re
import urllib2
import urlparse

HTML_REGEX = re.compile(r'((?:src|action|href)=["\'])/')
JQUERY_REGEX = re.compile(r'(\$\.(?:get|post)\(["\'])/')
JS_LOCATION_REGEX = re.compile(r'((?:window|document)\.location.*=.*["\'])/')
CSS_REGEX = re.compile(r'(url\(["\']?)/')
   
REGEXES = [HTML_REGEX, JQUERY_REGEX, JS_LOCATION_REGEX, CSS_REGEX]

# returns iter of tuples of elements in a multudict
def iterform(multidict):
  for key in multidict.keys():
    for value in multidict.getlist(key):
      yield (key.encode("utf8"), value.encode("utf8"))

# get the hostname and port from request header HTTP_HOST
def parse_host_port (h):
  host_port = h.split(":", 1)
  if len(host_port) == 1:
    return(h, 80)
  else:
    host_port[1] = int(host_port[1])
    return host_port

def proxy(request):
  # parse hostname and port 
  hostname, port = parse_host_port(request.HTTP_HOST)
  if request.method == "POST":
    form_data = list(iterform(request.POST))
    form_data = urllib2.urlencode(form_data)
    request_header["Content-Length"] = len(form_data)
  else:
    form_data = None

  # establish the conenction
  conn = httplib.HTTPConnection(hostname, port)

	return render(request, 'templates/output.html', ({}))
