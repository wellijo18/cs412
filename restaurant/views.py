from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time

# Create your views here.

daDailySpecials = [
    {
        "name": "Banana Split",
        "price": "$7.99",
    },
    {
        "name": "Brownie Sundae",
        "price": "$6.50",
    },
    {
        "name": "Cookie Dough Tornado",
        "price": "$5.99",
    },
    {
        "name": "Peanut Butter Banana Cup Shake",
        "price": "$6.25",
    },
]

def main(request):
  template_name = 'restaurant/main.html'
  context = {
    "pict": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7kBi-JrLrWcSw-cYIwSNZUfT1j1Pn-JSkdg&s",
  }
  return render(request, template_name, context)

def order_page(request):
  template_name = 'restaurant/order.html'

  # randomly choose the special for the day, maid it set so that the price would always be the same depending on the item

  daSpecial = random.choice(daDailySpecials)
    
  context = {
        "daSpecialName": daSpecial["name"],
        "daSpecialPrice": daSpecial["price"],
    }

  return render(request, template_name, context)

def submit(request):
  '''Process the submission and generate a result'''
  template_name = "restaurant/confirmation.html"

  # grab all the info passed from order page
  if request.POST:
    daName = request.POST['daName']
    daPhone = request.POST['daPhone']
    daEmail = request.POST['daEmail']
    daSoftServe = request.POST.get('daSoftServe', '')
    daMilkshake = request.POST.get('daMilkshake', '')
    daSundae = request.POST.get('daSundae', '')
    daDailySpecial = request.POST.get('daDailySpecial', '')
    softServeSize = request.POST.get('softServeSize', '')
    softServeToppings = request.POST.getlist('softServeToppings')
    milkshakeFlavor = request.POST.get('milkshakeFlavor', '')
    daSpecialName = request.POST.get('daSpecialName', '')
    daSpecialPrice = request.POST.get('daSpecialPrice', '')
  # calculate our total price (we have to convert string from daily special to float tho)
  total = 0.0
  if daSoftServe:
    total += 3.50
    if softServeSize == 'medium':
      total += 1.00
    elif softServeSize == 'large':
      total += 2.00
      
    for topping in softServeToppings:
      if topping == 'sprinkles':
        total += 0.50
      elif topping == 'chocolate':
        total += 0.75
      elif topping == 'cherry':
        total += 0.25
    
  if daMilkshake:
    total += 5.50
    
  if daSundae:
    total += 6.00
    
  if daDailySpecial and daSpecialPrice:
    daCurSP = float(daSpecialPrice.replace('$', ''))
    total += daCurSP

  # get random time between 30 and 60 min
  randomMin = random.randint(30,60)

  #convert to sec and add time to current time
  randomSec = time.time() + (randomMin * 60)

  #format to actually look good 
  randomReadytime = time.strftime("%I:%M %p", time.localtime(randomSec))


  # pass in all of our context so that we can display info on the confirmation page
  context = {
    'daName': daName,
    'daPhone': daPhone,
    'daEmail': daEmail,
    'daSoftServe': daSoftServe,
    'daMilkshake': daMilkshake,
    'daSundae': daSundae,
    'daDailySpecial': daDailySpecial,
    'softServeSize': softServeSize,
    'softServeToppings': softServeToppings,
    'milkshakeFlavor': milkshakeFlavor,
    'daSpecialName': daSpecialName,
    'daSpecialPrice': daSpecialPrice,
    'total': f"${total:.2f}",
    'readyTime': randomReadytime,
  }

  return render(request, template_name=template_name, context=context)