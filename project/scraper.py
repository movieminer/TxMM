import json
import os

import googleapiclient.discovery
import googleapiclient.errors

api_service_name = "youtube"
api_version = "v3"
key=os.environ.get('YOUTUBE_API_KEY')

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=key)

# Retrieve youtube videos
def retrieve_youtube_videos(search_terms, published_after, max_results=50, npt=None):
  try :
    request = youtube.search().list(
        part="snippet",
        channelType="any",
        maxResults=max_results,
        publishedAfter=published_after,
        q=search_terms,
        relevanceLanguage="nl",
        safeSearch="none",
        type="video",
        pageToken=npt
    )
    response = request.execute()
  except googleapiclient.errors.HttpError as e:
    raise Exception(e)

  return response

# Retrieve comments per video
def retrieve_comments_per_video(video_id):
  try :
    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        order="relevance",
        textFormat="plainText",
        videoId=video_id
    )
    response = request.execute()
  except googleapiclient.errors.HttpError as e:
    error_reason = json.loads(e.content.decode('utf-8'))['error']['errors'][0]['reason']

    if error_reason == 'commentsDisabled':
      print('Comments are disabled for this video, skipping ...')
      return None
    raise Exception(e)

  return response


def search_videos(terms):
    videos = retrieve_youtube_videos(terms, "2023-07-07T00:00:00Z")
    npt = videos.get('nextPageToken', None)
    videos_2 = retrieve_youtube_videos(terms, "2023-07-07T00:00:00Z", npt=npt)

    terms_f = terms.replace(' ', '_')
    with open(f'data/videos/videos_{terms_f}.json', 'w') as f:
      json.dump([videos, videos_2], f)

    return videos.get('nextPageToken', None)


def search_comments(terms):
  terms_f = terms.replace(' ', '_')
  with open(f'data/videos/videos_{terms_f}.json', 'r') as f:
    videos = json.load(f)

  video_ids = []
  for page in videos:
    for video in page['items']:
      if video['id']['kind'] == 'youtube#video':
        video_ids.append(video['id']['videoId'])  

  # Retrieve comments per video
  comments_disabled = []
  comments = []
  for video_id in video_ids:
    comments_per_video = retrieve_comments_per_video(video_id)
    if comments_per_video:
      comments.append(comments_per_video)
    else:
      comments_disabled.append(video_id)

  with open(f'data/comments/comments_{terms_f}.json', 'w') as f:
    json.dump(comments, f)

  with open(f'data/comments/comments_disabled_{terms_f}.json', 'w') as f:
    json.dump(comments_disabled, f)