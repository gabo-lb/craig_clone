import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
from . import models


BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/hhh?query={}'

# Create your views here.

def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    print("soup is {}".format(type(soup)))

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        print('post title: {}'.format(post_title))
        post_url = post.find('a').get('href')
        post_price = post.find(class_='result-price').text

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_postings.append((post_title, post_url, post_price))
    print(final_postings)
    stuff_for_fronend = {
        'search' : search,
        'final_postings' : final_postings,
    }

    return render(request, 'my_app/new_search.html', stuff_for_fronend)
