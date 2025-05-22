from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

all_quotes = [

       "Nobody exists on purpose. Nobody belongs anywhere. Everybody's gonna die. Come watch TV.",
       "To live is to risk it all; otherwise, you're just an inert chunk of randomly assembled molecules drifting wherever the universe blows you.",
       "I'm sorry, but your opinion means very little to me.",
       "You're not gonna believe this because it usually never happens, but I made a mistake.",
       "I’m not arguing, I’m explaining why I’m right.",
        "I know that's not a popular opinion, but that's my two cents on the issue." ,
       "There's a lesson here and I'm not going to be the one to figure it out."
        
]
    
all_images = [
    "image1.png",
    "image2.png",
    "image3.png",
    "image4.png",
]


def home(request):
    '''Define a view to show the 'home.html' template.'''

    # the template to which we will delegate the work
    template_name = 'quotes/home.html'

    context = {
        "date": time.strftime("%B %d, %Y"),
        "todaysQuote": random.choice(all_quotes),
        "todaysImage": random.choice(all_images),

    }
    
    return render(request, template_name, context)

def about(request):
    '''Define a view to show the 'about.html' template.'''

    # the template to which we will delegate the work
    template_name = 'quotes/about.html'

    context = {
        "date": time.strftime("%B %d, %Y"),

    }

    return render(request, template_name, context)

def showall(request):
    '''Define a view to show the 'showall.html' template.'''

    # the template to which we will delegate the work
    template_name = 'quotes/showall.html'

    context = {
        "date": time.strftime("%B %d, %Y"),
        "allQuotes": all_quotes,
        "allImages": all_images,
    }

    return render(request, template_name, context)

