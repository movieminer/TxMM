import json
import pandas as pd
import scraper as sc
import data as dt

queries = ["vvd", "pvv", "groenlinks | pvda | groenlinks pvda", "d66", "cda"]

# # for query in queries:
# #   sc.search_videos(query)
# #   sc.search_comments(query)

# for query in queries:
#   query = query.replace(' ', '_')
#   dt.save_pd_as_csv(dt.get_relevant_video_data("data/json/videos/videos_" + query + ".json"), 
#                     "data/csv/videos/videos_" + query + ".csv")
#   dt.save_pd_as_csv(dt.get_relevant_comment_data("data/json/comments/comments_" + query + ".json"),
#                      "data/csv/comments/comments_" + query + ".csv")

with open("data/csv/comments/comments_vvd.csv") as f:
  comments = pd.read_csv(f)

for c in comments['textDisplay']:
  print(c)
  print(dt.translate_comment(c))
  print()