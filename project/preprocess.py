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
comments = comments.drop_duplicates(subset=['videoId','textDisplay', 'authorDisplayName'])
print(comments.shape)