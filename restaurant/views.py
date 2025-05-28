# File: views.py
# Author: Veer Agrawal (veer1@bu.edu), 5/27/2025
# Description: Logic for rendering the main homepage, order page, and a confirmation page.


from django.shortcuts import render
import datetime
import time
import random

# Create your views here.

def home(request):
    """Render the homepage with the current date."""

    template_name = "restaurant/main.html"

    context = {
        "date": time.strftime("%B %d, %Y"),

    }

    return render(request, template_name, context)
 


def order(request):

    """Render the order page with a randomly selected daily special."""


    template_name = "restaurant/order.html"

    special_items = {
        "Dosa": 7.99, 
        "Dal makhani": 10.99, 
        "Biryani": 8.99
    }

    daily_special_name = random.choice(list(special_items.keys()))
    daily_special_price = special_items.get(daily_special_name)
    
    context = {
        "date": time.strftime("%B %d, %Y"),
        "daily_special_name": daily_special_name,
        "daily_special_price": daily_special_price

    }

    return render(request, template_name, context)

def confirmation(request):
    """Process the order form, calculate total, and render confirmation page."""

    template_name = "restaurant/confirmation.html"
    
    if request.POST:

        menu_items = {
            "Butter Chicken": 12.99,
            "Chicken Biryani": 11.99,
            "Samosa": 4.99,
            "Paneer Makhani": 10.99,
            "Garlic Naan": 3.49
        }


        # ading the daily special into menu_items for pricing
        daily_special_name = request.POST.get('daily_special_name')
        daily_special_price = float(request.POST.get('daily_special_price'))
        menu_items[daily_special_name] = daily_special_price

        minutes_to_add = random.randint(30, 60)
        orderTime = (datetime.datetime.now() + datetime.timedelta(minutes=minutes_to_add)).strftime("%I:%M %p")

        food_items = request.POST.getlist('food')         
        order_total = sum(menu_items[item] for item in food_items)

        instructions = request.POST['instructions']
        delivery_or_pickup = request.POST['d/p']
        address = request.POST['address']
        payment = request.POST['payment']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']

        context = {
            "date": time.strftime("%B %d, %Y"),
            "orderTime": orderTime,
            "food_items": food_items,
            "daily_special_name": daily_special_name,
            "daily_special_price": daily_special_price,
            "order_total": order_total,
            "instructions": instructions,
            "delivery_or_pickup": delivery_or_pickup,
            "address": address,
            "payment": payment,
            "name": name,
            "email": email,
            "phone": phone,
        }

    return render(request, template_name, context)