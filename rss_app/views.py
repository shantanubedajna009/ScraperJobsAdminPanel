from django.shortcuts import render
from rss_app.models import Added_Jobs, Check_Ads_One, Check_Ads_Two
from rss_app.forms import JobForm
from django.http import HttpResponseRedirect, HttpResponse
import time, subprocess, os, shutil, uuid, json, simplejson
from django.core.files.storage import default_storage
from django.conf import settings
from datetime import datetime
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db import connection
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('<h1>ACCOUNT NOT ACTIVE !!!</h1>')
        else:
            return HttpResponse('<h1>Wrong Credentials</h1>')
    else:
        return render(request, 'rss_app/login.html', {}) # empty dict cause using html form this time


def index(request):
    return render(request, 'rss_app/index.html')

@login_required
def add_job(request):

    form = JobForm()
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            #job.tempfile = request.FILES['tempfile']

            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

            job.date_created = date_time

            job.save()

            return list_job(request)


        else:
            raise Exception('Form is not valid')
    else:
        return render(request, 'rss_app/add_job.html', context={'form': form})

@login_required
def list_job(request):

    jobs = Added_Jobs.objects.all()

    return render(request, 'rss_app/list_job.html', context={"jobs": jobs})

@login_required
def delete_job(request, **kwargs):
    job = Added_Jobs.objects.get(pk=kwargs.get('pk'))

    job.delete()

    return list_job(request)


@login_required
def get_job(request, **kwargs):
    job = Added_Jobs.objects.get(pk=kwargs.get('pk'))

    sll = job.excluded_sellers

    sll = sll.split('||')

    print(sll)

    return render(request, 'rss_app/show_job.html', context={'job': job, 'sellers': sll})

@login_required
def update_job(request):

    #update sellers part
    if request.method=='POST' and 'sellersform' in request.POST:

        newseller = request.POST.get('newseller')
        job_id = request.POST.get('jobid')

        newseller = newseller.strip()

        job = Added_Jobs.objects.get(pk=job_id)

        if job.excluded_sellers and newseller:
            sll = job.excluded_sellers

            s_l = sll.split('||')

            if newseller not in s_l:

                sll = sll + '||' + newseller
                job.excluded_sellers = sll
                job.save()

        elif (not job.excluded_sellers) and newseller:
            job.excluded_sellers = newseller
            job.save()
        else:
            pass


        return get_job(request, pk=job.id)


    # Full update part
    if request.method=='POST':
        job_id = request.POST.get('jobid')
        jobname = request.POST.get('jobname')
        joblink = request.POST.get('joblink')

        job = Added_Jobs.objects.get(pk=job_id)

        if (jobname and len(jobname.strip()) > 1) and (joblink and len(joblink.strip()) > 2):

            job.name = jobname.strip()
            job.link = joblink.strip()

            job.save()

        return get_job(request, pk=job.id)


@login_required
def update_status(request, **kwargs):

    job = Added_Jobs.objects.get(pk=kwargs.get('pk'))

    if job.run_status == '1':
        job.run_status = '0'
    else:
        job.run_status = '1'

    job.save()

    return get_job(request, pk=job.id)


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]


def get_check_ads_one(request):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM rss_app_check_ads_one");
    myjson = dictfetchall(cursor)

    myjson = json.dumps(myjson)

    loaded_json = json.loads(myjson)

    return HttpResponse(simplejson.dumps(loaded_json), content_type='application/json')

def get_check_ads_two(request):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM rss_app_check_ads_two");
    myjson = dictfetchall(cursor)

    myjson = json.dumps(myjson)

    loaded_json = json.loads(myjson)

    return HttpResponse(simplejson.dumps(loaded_json), content_type='application/json')


def rss_get(request):
    return render(request, 'rss_app/rss_get.html')

def rss_two_get(request):
    return render(request, 'rss_app/rss_two_get.html')


class CustomFeedGenerator(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(CustomFeedGenerator, self).add_item_elements(handler, item)

        handler.startElement(u'description', {})

        handler.startElement(u'image', {})
        handler.addQuickElement(u"url", item['image_link'])
        handler.addQuickElement(u"title", 'Some Title')
        handler.addQuickElement(u"link", 'http://www.marktplaats.nl/')
        handler.endElement(u'image')

        handler.addQuickElement(u"seller_name", item['seller_name'])
        handler.addQuickElement(u"price", item['price'])

        handler.endElement(u'description')


class LatestPostsFeed(Feed):
    title = "www.marktplaats.nl"
    link = "/feeds/"
    description = "Updates on changes and additions to posts published in the starter."

    #feed_type = CustomFeedGenerator

    def items(self):
        return Check_Ads_One.objects.order_by('id')

    def item_description(self, item):
        return item.paragraph

    def item_title(self, item):
        return item.title

    #def item_extra_kwargs(self, item):

    #    return { 'image_link': item.image_link,
    #            'seller_name' : item.seller_name,
    #            'price': item.price,}

    def item_link(self, item):
        return item.prod_link


class LatestPostsFeedTwo(Feed):
    title = "Posts for bedjango starter"
    link = "/feedstwo/"
    description = "Updates on changes and additions to posts published in the starter."

    #feed_type = CustomFeedGenerator

    def items(self):
        return Check_Ads_Two.objects.order_by('id')

    def item_description(self, item):
        return item.paragraph

    def item_title(self, item):
        return item.title

    #def item_extra_kwargs(self, item):

    #    return { 'image_link': item.image_link,
    #            'seller_name' : item.seller_name,
    #            'price': item.price,}

    def item_link(self, item):
        return item.prod_link
