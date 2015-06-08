from requests import request, ConnectionError
from tyaffiliate.models import UserPages
from social.exceptions import AuthUnreachableProvider
from tyaffiliate.pipeline import save_image


def add_pages(strategy, details, response, user=None, *args, **kwargs):
    """Save user pages in UserPages table"""
    if user:
        # Check for all page_ids associated with user
        page_ids = list(UserPages.objects.filter(user=user).values('page_id'))

        if page_ids:
            page_ids = [page_id['page_id'] for page_id in page_ids]

        # Get response data
        user_id = response.get('id')
        access_token = response.get('access_token')
        url = 'https://graph.facebook.com/{0}/accounts?access_token={1}'.format(user_id, access_token)

        try:
            url_response = request('GET', url)
            accounts = url_response.json().get('data')
        except ConnectionError:
            raise AuthUnreachableProvider(kwargs['backend'])

        for data in accounts:
            if data['id'] not in page_ids:
                user_page_obj = UserPages(user=user)
                user_page_obj.page_id = data['id']
                user_page_obj.page_name = data['name']
                image_url = 'http://graph.facebook.com/{0}/picture?height=80&width=80'.format(data['id'])
                save_image(image_url, user_page_obj, data['id'])


# TODO
                # Extend method for Twitter and Google+