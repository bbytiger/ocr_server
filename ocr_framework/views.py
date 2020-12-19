from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import requests, os, base64, json
from PIL import Image, ImageFilter
from io import StringIO
import pytesseract

@api_view(['GET','POST'])
def text(request):
  if request.method == 'GET':
    return Response({"message": "Hello, you have reached the text endpoint! Issue a POST request to this endpoint and it will convert your image to text!"})
  elif request.method == 'POST':
    res = request.data
    b64_im = json.loads(res)['data']
    im = base64.b64decode(b64_im)
    if not os.path.isdir('tmp'):
      print("making directory")
      os.mkdir('tmp')
    tempfile = 'tmp/image_binary.txt'
    with open(tempfile, 'wb') as request_image:
      request_image.write(im)
    im = Image.open(tempfile)
    im.filter(ImageFilter.SHARPEN)
    text = pytesseract.image_to_string(im)
    if os.path.exists(tempfile):
      os.remove(tempfile)
    return Response({"text": text})

@api_view(['GET','POST']) 
def pdf(request):
  if request.method == 'GET':
    return Response({"message": "Hello, you have reached the pdf endpoint! Issue a POST request to this endpoint and it will return a searchable .pdf file!"})
  elif request.method == 'POST':
    res = request.data
    b64_im = json.loads(res)['data']
    im = base64.b64decode(b64_im)
    if not os.path.isdir('tmp'):
      print("making directory")
      os.mkdir('tmp')
    tempfile = 'tmp/image.png'
    returnfile = 'tmp/return.pdf'
    with open(tempfile, 'wb') as request_image:
      request_image.write(im)
    pdf = pytesseract.image_to_pdf_or_hocr(tempfile, extension='pdf')
    with open(returnfile, 'w+b') as f:
      f.write(pdf)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + returnfile + '"' 
    if os.path.exists(tempfile):
      os.remove(tempfile)
      os.remove(returnfile)
    return response