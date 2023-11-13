import json
import pandas as pd

# with open('data/youtube_videos.json') as f:
#   videos = json.load(f)

# # Convert to dataframe
# next_page_token = videos['nextPageToken']
# df = pd.DataFrame(videos['items'])
# id = df['id'].apply(pd.Series).reindex(columns=['videoId', 'kind'])
# snippet = df['snippet'].apply(pd.Series)

# data = pd.concat([id, snippet], axis=1).reindex(columns=['videoId', 'publishedAt', 'kind', 'title', 'description', 'channelTitle', 'liveBroadcastContent'])
# data['publishedAt'] = pd.to_datetime(data['publishedAt']).dt.date
# data.sort_values(by=['publishedAt'], inplace=True, ascending=True)
# print(data.head())

with open('data/youtube_comments.json', 'r') as f:
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
print(comment_data.head())