from requests import request, ConnectionError
from social.exceptions import AuthUnreachableProvider
from tyaffiliate.extensions.auth_extensions import AuthMissingParameterExtension
from datetime import datetime
import pytz

INSIGHTS_DATA = []
utc = pytz.UTC

def get_post_ids(access_token, page_id, backend, join_date):
    # Get feed of user's page to look for posted links
    url = 'https://graph.facebook.com/{0}/feed?access_token={1}'.format(page_id, access_token)
    data = []

    try:
        response = request('GET', url)
    except ConnectionError:
        raise AuthUnreachableProvider(backend)

    # Store feed data for links containing topyaps.com to perform facebook analytics
    for result in response.json().get('data'):
        created_time = utc.localize(datetime.strptime(result['created_time'], "%Y-%m-%dT%H:%M:%S+0000"))
        link = result.get("link")

        if link:
            if "topyaps.com" in link and join_date < created_time:
                topyaps_link = result['link'].split("?")[0] if "?" in result['link'] else result['link']
                data.append({"link": topyaps_link, "id": result["id"]})

    return data


def get_insights(access_token, data, backend):
    insight_data = {}

    # check if user has posted any topyaps links or not
    if not data:
        insight_data['error_message'] = "You have not posted any links of Topyaps on your page"
    else:
        for link in data:
            post_id = data[link]
            url = 'https://graph.facebook.com/{0}/insights?access_token={1}'.format(post_id, access_token)

            try:
                response = request('GET', url)
            except ConnectionError:
                raise AuthUnreachableProvider(backend)

            if not response.json().get('data'):
                raise AuthMissingParameterExtension(backend, parameter='read-insights')

            for insight in response.json().get('data'):
                if insight.get('name') in INSIGHTS_DATA:
                    insight_name = insight.get('name')
                    insight_value = insight.get('value')
                    if not link in insight_data:
                        insight_data[link] = [{insight_name: insight_value}]
                    else:
                        insight_data[link].append({insight_name: insight_value})

    return insight_data


def get_page_data(access_token, page_id, backend):
    page_data = {}
    url = 'https://graph.facebook.com/{0}?access_token={1}'.format(page_id, access_token)

    try:
        response = request('GET', url)
    except ConnectionError:
        raise AuthUnreachableProvider(backend)

    page_data['likes'] = response.json().get('likes')
    page_data['talking_about_count'] = response.json().get('talking_about_count')

    return page_data