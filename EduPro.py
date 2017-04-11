
'''
Created on Apr 11, 2017

@author: HackPirateers
'''

import httplib2

import os

import re

import sys



from apiclient.discovery import build #pip install google-api-python-client

from apiclient.errors import HttpError #pip install google-api-python-client

from oauth2client.tools import argparser #pip install oauth2client

import pandas as pd #pip install pandas

import pandasql as pdsql #pip install pandasql

import matplotlib as plt

from pandas.tools.util import to_numeric



DEVELOPER_KEY = "AIzaSyAjn2lRpYw3mQr4-U1y5MzRazINXhrDlcg" 

YOUTUBE_API_SERVICE_NAME = "youtube"

YOUTUBE_API_VERSION = "v3"

argparser.add_argument("--q", help="science", default="how to learn java")

#change the default to the search term you want to search

argparser.add_argument("--max-results", help="Max results", default=25)



#default number of results which are returned. It can vary from 0 - 100

args = argparser.parse_args()

options = args

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

# Call the search.list method to retrieve results matching the specified

 # query term.

search_response = youtube.search().list(

 q=options.q,

 type="video",

 part="id,snippet",

 maxResults=options.max_results

).execute()

videos = {}

# Add each result to the appropriate list, and then display the lists of

 # matching videos.

 # Filter out channels, and playlists.

for search_result in search_response.get("items", []):

 if search_result["id"]["kind"] == "youtube#video":

 #videos.append("%s" % (search_result["id"]["videoId"]))

  videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

# print "Videos:\n", "\n".join(videos), "\n"

s = ','.join(videos.keys())

videos_list_response = youtube.videos().list(

 id=s,

 part='id,statistics'

).execute()

#videos_list_response['items'].sort(key=lambda x: int(x['statistics']['likeCount']), reverse=True)

#res = pd.read_json(json.dumps(videos_list_response['items']))



res = []

for i in videos_list_response['items']:

 temp_res = dict(v_id = i['id'], v_title = videos[i['id']])

 temp_res.update(i['statistics'])



 res.append(temp_res)

print res

pd.DataFrame.from_dict(res)

df =  pd.DataFrame(res,columns=["viewCount","v_title" , "commentCount","v_id" , "likeCount","dislikeCount"])

print res

#print df

df['viewCount'] = df['viewCount'].astype('float') 

#df['favoriteCount'] = df['favoriteCount'].astype('int64')

df['commentCount'] = df['commentCount'].astype('float') 

df['likeCount'] = df['likeCount'].astype('float')

df['dislikeCount'] = df['dislikeCount'].astype('float') 

df['likeCount'] = ( df['likeCount'] - df['dislikeCount']/df['likeCount'])

#df['likeCount'] = df['likeCount'].astype('int64')

#print df

pysql = lambda q: pdsql.sqldf(q, globals())

#str1 = "select viewCount,commentCount,v_id,v_title,likeCount from df order by viewCount DESC,commentCount DESC, likeCount DESC limit 10"

str1 = "select viewCount,commentCount,v_id,v_title,likeCount from df order by likeCount DESC, v_title DESC, viewCount DESC,commentCount DESC limit 10"





df1 = pysql(str1)

print df1