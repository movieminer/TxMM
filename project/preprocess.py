import json
import pandas as pd
import scraper as sc
import data as dt
import numpy as np
import time

with open("data/csv/comments/comments.csv", "r") as f:
  comments = pd.read_csv(f)

print(comments.shape)
comments = comments.drop_duplicates()
print(comments.shape)
comments = comments.drop_duplicates(subset=['textDisplay', 'authorDisplayName'])
print(comments.shape)
comments = comments.sort_values(by=['publishedAt'], ascending=True)
print(comments.head(10))

# Return subset of comments from specific months
def get_comments_by_month(comments, month):
  return comments[comments['publishedAt'].str.contains(f'2023-{month}-')]

months = ['07', '08', '09', '10', '11']

for month in months:
  print(get_comments_by_month(comments, month).shape)