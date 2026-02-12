from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
quotes = [
  "If peeing your pants is cool, consider me Miles Davis",
  "YOU'RE GONNA DIE CLOWN",
  "The price is wrong bitch",
  ]

pics = [
  "https://www.usmagazine.com/wp-content/uploads/2023/07/Adam-Sandler-Style-Gallery-.jpg?quality=70&strip=all",
  "https://media.cnn.com/api/v1/images/stellar/prod/230321113631-01-adam-sandler-restricted.jpg?q=w_3000,c_fill",
  "https://mediaproxy.tvtropes.org/width/1200/https://static.tvtropes.org/pmwiki/pub/images/r_34.jpg",
]
# Create your views here.

def quote(request):
  template_name = "quotes/quote.html"
  context = {
    "pict": random.choice(pics),
    "quot": random.choice(quotes),
  }
  return render(request, template_name, context)

def show_all(request):
  template_name = "quotes/show_all.html"
  # context specific allq and allp for going through all qutoes and pictures
  context ={
    "pict": random.choice(pics),
    "quot": random.choice(quotes),
    "allq": quotes,
    "allp": pics,
  }
  return render(request, template_name, context)

def about(request):
  template_name = "quotes/about.html"
  context ={
    "pict": random.choice(pics),
    "quot": random.choice(quotes),
  }
  return render(request, template_name, context)