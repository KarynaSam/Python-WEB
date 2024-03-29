import os

import django
import requests
from bs4 import BeautifulSoup
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Quote, Author, Tag
from .utils import get_mongodb
from .forms import AuthorForm, QuoteForm, TagForm


# def main(request, page=1):
#     db = get_mongodb()
#     quotes = db.quotes.find()
#     per_page = 10
#     paginator = Paginator(list(quotes), per_page)
#     quotes_on_page = paginator.page(page)
#
#     return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

def home(request, page=1):
    quotes = Quote.objects.all()
    per_page = 5
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    top_tags = Quote.objects.values('tags__name').annotate(quote_count=Count('tags__name')).order_by('-quote_count')[
               :10]
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page, 'top_tags': top_tags})


def author_about(request, _id):
    author = Author.objects.get(pk=_id)
    return render(request, 'quotes/author.html', context={'author': author})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            return redirect(to='quotes:home')
        else:
            return render(request, 'super_quotes/add_quote.html',
                          context={'form': QuoteForm, 'message': "Error"})
    return render(request, 'quotes/add_quote.html', context={'form': QuoteForm()})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save()
            return redirect(to='quotes:home')
        else:
            return render(request, 'quotes/add_author.html',
                          context={'form': AuthorForm, 'message': "Error"})
    return render(request, 'quotes/add_author.html', context={'form': AuthorForm()})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            new_tag = form.save()
            return redirect(to='quotes:home')
        else:
            return render(request, 'quotes/add_tag.html',
                          context={'form': TagForm, 'message': "Error"})
    return render(request, 'quotes/add_tag.html', context={'form': TagForm})


def find_tag(request, _id):
    per_page = 5
    if isinstance(_id, int):
        quotes = Quote.objects.filter(tags=_id).all()
    elif isinstance(_id, str):
        tag_id = Tag.objects.filter(name=_id).first()
        quotes = Quote.objects.filter(tags=tag_id).all()
    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    top_tags = Quote.objects.values('tags__id', 'tags__name').annotate(quote_count=Count('tags__name')).order_by(
        '-quote_count')[:10]

    return render(request, 'quotes/find_tag.html',
                  context={'quotes': page_obj, 'tag_name': _id, 'top_tags': top_tags})


def search_quotes(request):
    query = request.GET.get('q')
    quotes = Quote.objects.filter(
        Q(tags__name__icontains=query) |
        Q(quote__icontains=query) |
        Q(author__fullname__icontains=query)
    ).distinct()

    return render(request, 'quotes/search_quotes.html', context={'quotes': quotes, 'query': query})


@login_required()
def parse(request):
    base_url = 'http://quotes.toscrape.com'

    def get_author_urls():
        author_links = []
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        for q in quotes:
            author_links.append(q.find("a", href=True).get('href'))
        return author_links

    def quote_spider():
        created_quotes = []
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select('div[class=col-md-8] div[class=quote]')
        for el in content:
            quote_text = el.find('span', attrs={'class': 'text'}).text
            author_fullname = el.find('small', attrs={'class': 'author'}).text
            author, created = Author.objects.get_or_create(fullname=author_fullname)

            tags = (list(filter(bool, [t.text.strip() for t in el.find('div', class_='tags').find_all('a')])))

            new_quote, created = Quote.objects.get_or_create(quote=quote_text, author=author)
            if created:
                for tag_name in tags:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    new_quote.tags.add(tag)
            new_quote.save()
            created_quotes.append(new_quote)
        return created_quotes

    def author_spider():
        author_links = get_author_urls()
        created_authors = []
        for link in author_links:
            response = requests.get(base_url + link)
            soup = BeautifulSoup(response.text, 'lxml')
            content = soup.select('div[class=container] div[class=author-details]')
            for el in content:
                fullname = el.find('h3', attrs={'class': 'author-title'}).text.strip()
                date_born = el.find('span', attrs={'class': 'author-born-date'}).text.strip()
                born_location = el.find('span', attrs={'class': 'author-born-location'}).text.strip()
                bio = el.find('div', attrs={'class': 'author-description'}).text.strip()
                author, created = Author.objects.get_or_create(fullname=fullname, date_born=date_born,
                                                               born_location=born_location,
                                                               bio=bio)
                author.save()
                created_authors.append(author)
        return created_authors

    def parsing():
        return author_spider(), quote_spider()

    return render(request, 'quotes/parse.html', context={'final_parse': parsing, 'base_url': base_url})
