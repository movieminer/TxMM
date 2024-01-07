import json
import pandas as pd
import scraper as sc
import data as dt
import numpy as np
import time

queries = ["vvd", "pvv", "groenlinks | pvda | groenlinks pvda", "d66", "cda"]

def get_relevant_video_data(queries):
  for query in queries:
    sc.search_videos(query)
    sc.search_comments(query)

    query = query.replace(' ', '_')
    dt.save_pd_as_csv(dt.get_relevant_video_data("data/json/videos/videos_" + query + ".json"), 
                      "data/csv/videos/videos_" + query + ".csv")
    dt.save_pd_as_csv(dt.get_relevant_comment_data("data/json/comments/comments_" + query + ".json"),
                      "data/csv/comments/comments_" + query + ".csv")

def translate_comments(queries):
  for q in queries:
    q = q.replace(' ', '_')
    with open(f"data/csv/comments/comments_{q}.csv", "r") as f:
      comments = pd.read_csv(f)

    try:
      comments['textTranslated'] = comments['textDisplay'].apply(dt.translate_comment)
    except Exception:
      dt.save_pd_as_csv(comments, f"data/csv/comments/comments_{q}.csv")
      print("Waiting 30 seconds...")
      time.sleep(30)
      comments['textTranslated'] = comments['textDisplay'].apply(dt.translate_comment)

    dt.save_pd_as_csv(comments, f"data/csv/comments/comments_{q}.csv")


def merge_comments_to_one_file(queries):
  comments = pd.DataFrame()
  for q in queries:
    q = q.replace(' ', '_')
    path = f'data/csv/comments/comments_{q}.csv'
    df = pd.read_csv(path)
    comments = pd.concat([comments, df], ignore_index=True)

  comments.to_csv('data/csv/comments/comments.csv', index=False)

merge_comments_to_one_file(queries)