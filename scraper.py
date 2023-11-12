import json
import os

import googleapiclient.discovery
import googleapiclient.errors

api_service_name = "youtube"
api_version = "v3"
key=os.environ.get('YOUTUBE_API_KEY')

youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=key)

# Retrieve youtube videos
def retrieve_youtube_videos(search_terms, published_after, max_results=50):
  try :
    request = youtube.search().list(
        part="snippet",
        channelType="any",
        maxResults=max_results,
        publishedAfter=published_after,
        q=search_terms,
        relevanceLanguage="nl",
        safeSearch="none",
        type="video"
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


# videos = retrieve_youtube_videos("verkiezingen | tweede kamerverkiezingen | vvd | pvv | fvd | groenlinks", "2023-07-07T00:00:00Z")

# with open('youtube_videos.json', 'w') as f:
#   json.dump(videos, f)

with open('youtube_videos.json', 'r') as f:
  videos = json.load(f)

video_ids = [videos['items'][x]['id']['videoId'] for x in range(len(videos['items']))]

# Retrieve comments per video
comments_disabled = []
comments = []
for video_id in video_ids:
  comments_per_video = retrieve_comments_per_video(video_id)
  if comments_per_video:
    comments.append(comments_per_video)
  else:
    comments_disabled.append(video_id)

with open('youtube_comments.json', 'w') as f:
  json.dump(comments, f)

with open('youtube_comments_disabled.json', 'w') as f:
  json.dump(comments_disabled, f)