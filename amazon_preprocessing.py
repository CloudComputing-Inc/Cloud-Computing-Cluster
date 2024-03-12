#data source for All_Amazon_Review_5.json.gz 
#https://nijianmo.github.io/amazon/

import pandas as pd
import gzip
import json
from numpy import random
from sqlalchemy import create_engine

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield json.loads(l)

def getDF(path):
  rng = random.default_rng(123)
  i = 0
  df = {}
  for d in parse(path):
    if (rng.binomial(n=1, p=0.02) == 1):
      df[i] = d
      i += 1
  return pd.DataFrame.from_dict(df, orient='index')

reduced_df = getDF('data/All_Amazon_Review_5.json.gz')

with open('data/amazon_reviews_reduced.json', mode='w') as file:
  reduced_df.to_json(path_or_buf=file, orient='records', lines=True)

reduced_df[['style', 'image']] = reduced_df[['style', 'image']].astype(str)

engine = create_engine('sqlite:///data/amazon.db')
reduced_df.to_sql(name='reviews', con=engine)