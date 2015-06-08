from django.shortcuts import redirect, render, render_to_response
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.messages import get_messages
from django.http import HttpResponse

from .models import UserPages, UserProfile, UserPagePosts
from .data_retrievers.analytics_data import get_realtime_data
from .data_retrievers.insights_data import get_post_ids, get_page_data

import requests
import json


# Create your views here.


def login(request):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        storage = get_messages(request)
        if not storage:
            return render(request, 'tyaffiliate/login.html')
        else:
            return render_to_response('tyaffiliate/login.html', {
                'message': storage
            }, context_instance=RequestContext(request))


@login_required(login_url='/login')
def home(request):
    return render(request, 'tyaffiliate/home.html')


@login_required(login_url='/login')
def search(request):
    return render(request, 'tyaffiliate/search.html')


@login_required(login_url='/login')
def accounts(request):
    user = request.user
    user_profile = UserProfile.objects.filter(user=user)
    user_pages = UserPages.objects.filter(user=user)

    return render_to_response('tyaffiliate/accounts.html', {
        'profile': user_profile,
        'pages': user_pages
    }, context_instance=RequestContext(request))


@login_required(login_url='/login')
def view_published_posts(request, page_id):
    return render(request, 'tyaffiliate/published.html')


@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    return redirect('/login')


def extra_data(user):
    facebook = user.social_auth.get(provider='facebook')
    backend = facebook.get_backend_instance()
    access_token = facebook.extra_data['access_token']
    return [access_token, backend]


def get_google_data(request):
    if request.method == "GET":
        google_data = get_realtime_data()
        return HttpResponse(
            json.dumps(google_data),
            content_type="application/json"
        )


def get_topyaps_data(request):
    if request.method == "GET":
        data = []
        params = request.GET.get('param')
	url = "http://topyaps.com/app-webservices/post_list_all.php?list_type=" + params
        resp = requests.get(url)

        if resp.json().get('payload'):
            for ty_data in resp.json().get('payload'):
                data.append({
                    "post_title": ty_data["post_title"],
                    "post_url": "http://topyaps.com/" + ty_data["post_name"],
                    "post_date": ty_data["post_date_db"].split()[0],
                    "img_url": ty_data["featured_image"]
                })

            return HttpResponse(
                json.dumps(data),
                content_type="application/json"
            )


def page_additional_data(request):
    if request.method == "GET":
        user = request.user
        data = extra_data(user)

        page_id = request.GET.get("id")
        page_data = get_page_data(data[0], page_id, data[1])

        return HttpResponse(
            json.dumps(page_data),
            content_type="application/json"
        )


def sync_posts(request):
    if request.method == "POST":
        response_data = {}
        user = request.user
        data = extra_data(user)

        page_id = request.POST.get('post_id')
        post_data = get_post_ids(data[0], page_id, data[1], user.date_joined)

        page = UserPages.objects.filter(page_id=page_id)[0]
        page_post_urls = [url_val['post_url'] for url_val in UserPagePosts.objects.filter(page=page).values('post_url')]

        if post_data:
            for ty_data in post_data:
                if ty_data["link"] not in page_post_urls:
                    post = UserPagePosts(page=page)
                    post.post_url = ty_data["link"]
                    post.post_id = ty_data["id"]
                    post.save()

            response_data['message'] = "success"

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            response_data['message'] = "danger"

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )


def get_published_posts(request):
    if request.method == "GET":
        data = []
        page_id = request.GET.get('id')

        page = UserPages.objects.filter(page_id=page_id)
        posts = UserPagePosts.objects.filter(page=page)

        for ty_data in posts:
            data.append({"link": ty_data.post_url, "view": ty_data.post_id})

        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )
