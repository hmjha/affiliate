import httplib2
from googleapiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

from affiliate.settings import KEY_FILE_PATH
from app_config.config import SERVICE_ACCOUNT_EMAIL


def get_service(api_name, api_version, scope, key_file_location, service_account_email):
    """Get a service that communicates to a Google API.

    Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

    Returns:
    A service that is connected to the specified API.
    """

    f = open(key_file_location, 'rb')
    key = f.read()
    f.close()

    credentials = SignedJwtAssertionCredentials(service_account_email, key, scope=scope)
    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.
    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property_id = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                accountId=account,
                webPropertyId=property_id
            ).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return None


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return service.data().realtime().get(
        ids='ga:' + profile_id,
        metrics='rt:pageviews',
        dimensions='rt:pagePath',
        max_results=20,
        sort='-rt:pageviews'
    ).execute()


def get_realtime_data():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

    # Use the developer console and replace the values with your
    # service account email and relative location of your key file.
    service_account_email = SERVICE_ACCOUNT_EMAIL
    key_file_location = KEY_FILE_PATH

    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, key_file_location, service_account_email)
    profile = get_first_profile_id(service)

    # Get results
    results = get_results(service, profile)
    data = []

    if not service or not profile or not results:
        data["error_message"] = "Could not get Google Analytics data"
    else:
        for result in results.get('rows'):
            url = "http://topyaps.com" + (result[0].split('?')[0] if "?" in result[0] else result[0])
            data.append({"link": url, "view": int(result[1])})

    return data