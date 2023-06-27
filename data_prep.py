import re
from hazm import *

def persian_only(input_csv):
    with open(input_csv, 'r') as input_file:
        tweets = "".join(" ".join(re.findall(r"[\u0620-\u065F\u066E-\u06EF\u06FA-\u06FF\n\#]+", line)) for line in input_file)
        tweets = tweets.replace("-", "")
        input_file.close()
    return tweets

def normalize_tweets(tweets, outfile):
    normalizer = Normalizer()
    normalized_tweets = normalizer.normalize(tweets)
    with open(outfile, "a") as output_file:
        output_file.write(normalized_tweets)