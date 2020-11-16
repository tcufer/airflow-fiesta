SELECT screen_name, content, favorite_count, retweet_count, created
FROM twitter_data
ORDER BY favorite_count DESC, retweet_count DESC