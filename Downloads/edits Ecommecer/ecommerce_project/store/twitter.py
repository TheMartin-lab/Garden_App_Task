import os
from django.conf import settings
try:
    import tweepy  # type: ignore
except Exception:
    tweepy = None

def _get_credentials():
    """Retrieve Twitter credentials from environment variables."""
    return {
        'api_key': os.getenv('TWITTER_API_KEY'),
        'api_secret': os.getenv('TWITTER_API_SECRET'),
        'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
        'access_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    }

def _get_api_v1(creds):
    """Get Twitter API v1.1 instance (for media upload)."""
    if tweepy is None or not all(creds.values()):
        return None
    auth = tweepy.OAuth1UserHandler(
        creds['api_key'], creds['api_secret'],
        creds['access_token'], creds['access_secret']
    )
    return tweepy.API(auth)

def _get_client_v2(creds):
    """Get Twitter API v2 Client instance (for posting tweets)."""
    if tweepy is None or not all(creds.values()):
        return None
    return tweepy.Client(
        consumer_key=creds['api_key'],
        consumer_secret=creds['api_secret'],
        access_token=creds['access_token'],
        access_token_secret=creds['access_secret']
    )

def post_tweet(text, media_path=None):
    """
    Post a tweet with optional media.
    Uses v2 Client for text and v1.1 API for media upload.
    """
    if not getattr(settings, 'TWITTER_ENABLED', False):
        return

    creds = _get_credentials()
    client = _get_client_v2(creds)
    if not client:
        return

    media_id = None
    # Try to upload media if provided
    if media_path and os.path.exists(media_path):
        api = _get_api_v1(creds)
        if api:
            try:
                media = api.media_upload(filename=media_path)
                media_id = media.media_id
            except Exception as e:
                print(f"Media upload failed: {e}")

    # Post the tweet
    try:
        if media_id:
            client.create_tweet(text=text, media_ids=[media_id])
        else:
            client.create_tweet(text=text)
    except Exception as e:
        print(f"Failed to send tweet: {e}")

def tweet_store(store):
    """Format and send a tweet for a new store."""
    text = f"New store: {store.name}\n{store.description}".strip()
    media = store.logo.path if store.logo else None
    post_tweet(text, media)

def tweet_product(product):
    """Format and send a tweet for a new product."""
    text = f"New product at {product.store.name}: {product.name}\n{product.description}".strip()
    media = product.image.path if product.image else None
    post_tweet(text, media)
