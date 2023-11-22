import json
import pandas as pd
from google.cloud import translate_v2


def get_relevant_video_data(path):
  with open(path) as f:
    videos = json.load(f)

  result = pd.DataFrame()

  for page in videos:
    # Convert to dataframe
    df = pd.DataFrame(page['items'])
    id = df['id'].apply(pd.Series).reindex(columns=['videoId', 'kind'])
    snippet = df['snippet'].apply(pd.Series)

    data = pd.concat([id, snippet], axis=1).reindex(columns=['videoId', 'publishedAt', 'kind', 'title', 'description', 'channelTitle', 'liveBroadcastContent'])
    data['publishedAt'] = pd.to_datetime(data['publishedAt']).dt.date
    result = pd.concat([result, data], ignore_index=True)
  
  result.sort_values(by=['publishedAt'], inplace=True, ascending=True)

  return result


def get_relevant_comment_data(path):
  with open(path, 'r') as f:
    comment_threads = json.load(f)

  # Convert to dataframe
  comments = pd.DataFrame()
  for comment_thread in comment_threads:
    for comment in comment_thread['items']:
      ct = comment['snippet']['topLevelComment']
      comments = comments._append(ct, ignore_index=True)


  comment_id = comments['id'].rename('commentId')
  snippet = comments['snippet'].apply(pd.Series)
  comment_data = pd.concat([comment_id, snippet], axis=1).reindex(columns=['commentId', 'videoId', 'publishedAt', 'authorDisplayName', 'textDisplay'])
  comment_data.set_index('commentId', inplace=True)
  comment_data['publishedAt'] = pd.to_datetime(comment_data['publishedAt']).dt.date
  comment_data.sort_values(by=['publishedAt', 'videoId'], inplace=True, ascending=[True, False])
  comment_data['textDisplay'] = comment_data['textDisplay'].apply(lambda x: x.replace('\n', ' ').replace('\r', ' '))

  return comment_data


def save_pd_as_csv(data, path):
  data.to_csv(path, index=False)


def translate_comment(comment):
  translate_client = translate_v2.Client()
  result = translate_client.translate(comment, target_language='en', source_language='nl')
  return result