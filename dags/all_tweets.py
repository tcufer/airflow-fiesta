#!/usr/bin/env python
# encoding: utf-8
# source: https://gist.github.com/onmyeoin/62c72a7d61fc840b2689b2cf106f583c

import tweepy
import csv
import pdb

def get_all_tweets(screen_name):

  consumer_key = ""
  consumer_secret = ""
  access_key = ""
  access_secret = ""

  #authorize twitter, initialize tweepy
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_key, access_secret)
  api = tweepy.API(auth, wait_on_rate_limit=True)

  #initialize a list to hold all the tweepy Tweets & list with no retweets
  alltweets = []
  noRT = []

  #make initial request for most recent tweets with extended mode enabled to get full tweets
  new_tweets = api.user_timeline(screen_name = screen_name, tweet_mode = 'extended', count=200)

  #save most recent tweets
  alltweets.extend(new_tweets)

  #save the id of the oldest tweet less one
  oldest = alltweets[-1].id - 1

  #keep grabbing tweets until the api limit is reached
  while len(alltweets) <= 1000:
    print("getting tweets before {}".format(oldest))
    # pdb.set_trace()

    #all subsiquent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(screen_name = screen_name,tweet_mode = 'extended', count=200,max_id=oldest)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    print("...{} tweets downloaded so far".format(len(alltweets)))

    #removes retweets
  for tweet in alltweets:
    if 'RT' in tweet.full_text:
      continue
    else:
      noRT.append([tweet.id_str, tweet.created_at, tweet.full_text])

  #write to csv
  with open('{}_tweets.csv'.format(screen_name), 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["id","created_at","text"])
    writer.writerows(noRT)
    print('{}_tweets.csv was successfully created.'.format(screen_name))
  pass


if __name__ == '__main__':
  #pass in the username of the account you want to download
  get_all_tweets("")
