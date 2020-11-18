SELECT screen_name, content, favorite_count, retweet_count, created
FROM twitter_data
ORDER BY favorite_count DESC, retweet_count DESC



SELECT extract(year from created) as year, screen_name, length(content) as tweet_length
FROM twitter_data
GROUP BY 1,3