import json
import pandas as pd
import scraper as sc
import data as dt

queries = ["pvv", "groenlinks | pvda | groenlinks pvda", "d66", "cda"]

# # for query in queries:
# #   sc.search_videos(query)
# #   sc.search_comments(query)

# for query in queries:
#   query = query.replace(' ', '_')
#   dt.save_pd_as_csv(dt.get_relevant_video_data("data/json/videos/videos_" + query + ".json"), 
#                     "data/csv/videos/videos_" + query + ".csv")
#   dt.save_pd_as_csv(dt.get_relevant_comment_data("data/json/comments/comments_" + query + ".json"),
#                      "data/csv/comments/comments_" + query + ".csv")

for q in queries:
  with open(f"data/csv/comments/comments_{q}.csv", "r") as f:
    comments = pd.read_csv(f)

  comments['textTranslated'] = comments['textDisplay'].apply(dt.translate_comment)
  

  dt.save_pd_as_csv(comments, f"data/csv/comments/comments_{q}.csv")