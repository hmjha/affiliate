from tyaffiliate.pipeline import save_image
from tyaffiliate.models import UserProfile


def save_profile(strategy, details, response, user=None, *args, **kwargs):
    """Save profile photo in profiles directory if doesn't exist"""
    if user:
        # Check if profile exists
        profile = UserProfile.objects.filter(user=user)

        if not profile:
            # Instantiate new profile
            prof = UserProfile(user=user)

            if kwargs['backend'].__class__.__name__ == 'FacebookOauth2Extension':
                url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
                save_image(url, prof, str(user.username))

            elif kwargs['backend'].__class__.__name__ == 'GoogleOAuth2':
                if response.get('image') and response['image'].get('url'):
                    url = response['image'].get('url').replace[:-5] + "sz=73"
                    save_image(url, prof, str(user.username))

            elif kwargs['backend'].__class__.__name__ == 'TwitterOAuth':
                if response.get('profile_image_url'):
                    url = response.get('profile_image_url', '').replace('_normal', '_bigger')
                    save_image(url, prof, str(user.username))