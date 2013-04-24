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
#log_file = open("log.txt", "rw")

# returns iter of tuples of elements in a multudict
def iterform(multidict):
  for key in multidict.keys():
    for value in multidict[key]:
      yield (key.encode("utf8"), value.encode("utf8"))

# get the hostname and port from request header HTTP_HOST
def parse_host_port (h):
  host_port = h.split(":", 1)
  if len(host_port) == 1:
    return(h, 80)
  else:
    host_port[1] = int(host_port[1])
    return host_port

def clean_and_split(content):
  #returns a list of [head,pre,post] without the doctype stuff

  #relevant regexes
  REMOVE_DOCTYPE = re.compile ( '(?P<doctype><!DOCTYPE((.|\n|\r)*?)\">)')
  INSERT_AD = re.compile ('(?P<head>.*<\s*HEAD[^<]*>)(?P<pre>.*<\s*BODY[^<]*>)(?P<post>.*)', re.IGNORECASE | re.MULTILINE | re.DOTALL)

  tmp = content
  
  #removes the doctype
  try: 
    tmp = re.sub(REMOVE_DOCTYPE, "", tmp)
  except:
    tmp = tmp  

  #splits
  try:
    split = INSERT_AD.match(tmp)
    head = split.group('head')
    pre = split.group('pre')
    post = split.group('post')
  except:
    head = "Error "
    pre = "Error "
    post = "Error "

  return (head, pre, post)




def proxy(request):
  server  = request.META["HTTP_HOST"]
  path = request.get_full_path()

  # parse hostname and port 
  hostname, port = parse_host_port(server)

  full_host = request.get_host()

  #parse out the headers that are relevant to pass onto the end server
  request_headers = {}
  for h in ["Cookie", "Referer", "X-Csrf-Token"]:
    if h in request.META.items():
      request_headers[h] = request.headers[h]
  

  if request.method == "POST":
    form_data = list(iterform(request.POST))
    form_data = urllib2.urlencode(form_data)
    request_header["Content-Length"] = len(form_data)
  else:
    form_data = None

  url = request.build_absolute_uri() 
  # get response and content from original destination
  h = httplib2.Http()
  resp, content = h.request("http://ntumma.com", request.method, body = form_data, headers = request_headers) 
  print resp

  # need to figure out how to modify the headers
  #response_headers = Headers()
  #for key, value in resp.getheaders():
  #  if key in ["content-length", 'connection', 'content-type']:
  #    continue
#
#    if key == 'set-cookie':
#      cookies = value.split(',')
#      [response_headers.add(key, c) for c in cookies]
#    else:
#      response_headers.add(key, value)
  
  # don't really know what to do in case of redirect, should test this out
#  if 'location' in response_headers:
#    redirect = response_headers['location']
#    parsed=  urlparse.urlparse()

  # process content in two stages

  #first change resource urls to absolute urls
  #root = url_for (".proxy_request", host = full_host)
  #urlparse.urljoin(url, link)
  print content
  # construct the response object from the template 

  #head, body, data = type = survey

  response = render(request, 'mysite/output.html', ({"url": url, "content" : content}))

  # modify response headers here

  # return response to client
  return response
