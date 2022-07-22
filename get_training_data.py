import json
import csv

# /////////////////// /////////////////// ///////////////////
dataset_path = '../_datasets'
dataset = 'charlemagne-jaehaerys'
#dataset = 'cyrus-daeron'
#dataset = 'ramses-maegor'
#dataset = 'sargon-solomon'
jsonfile = 'tweets-21-01'
# /////////////////// /////////////////// ///////////////////
s = 1600000 #start reading from line s...
t = 1959233 #... till line t
#tweets-21-01.json	5.31 GB		1959233
# /////////////////// /////////////////// ///////////////////
tweetsfile = dataset_path + '/' + dataset + '/' + jsonfile + '.json'

lookupfile = "../twitter/lookup_hashtags.csv"
outfile = '../twitter/train1.csv'
# /////////////////// /////////////////// ///////////////////
def to_file(tweets):
    with open("../twitter/debug.txt", "w", encoding="utf-8") as file:
        file.write(f"DATASET: {dataset}\n")
        file.write(f"FILE: {jsonfile}\n")
        for tweet in tweets:
            file.write(f"id: {tweet['id']}\n")
            file.write(f"content: {tweet['content']}\n")
            file.write(f"hashtags: {tweet['hashtags']}\n")
            file.write("------------\n") 

def load_lookup():
    lookup = []
    with open(lookupfile,'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for line in reader:
            #line = ['1', '#vacina', '63.519', 'in favor', 'neutral', '0', 'in favor', '']
            #line[1] = '#vacina'
            #line[6] = 'in favor'
            hashtag = line[1]
            hashtag = hashtag[1:] # remove first character '#'
            classification = line[6]
            lookup.append( (hashtag, classification) )
    lookup.pop(0) # remove header
    return lookup

def from_lookup(lookup, hashtags):
    for pair in lookup:
        # pair[0]: a string (hashtag)
        # pair[1]: a string (class)
        # hashtags: a list of strings
        if (pair[0] in hashtags) and (pair[1] != 'off-topic'):
            return (pair[0],pair[1])
    return None
           
def load_tweets(start=1, end=50): 
    #default behaviour: reading from line 1 (inclusive) to line 50 (inclusive)
    start = start - 1
    end = end - 1
    tweets = []
    #for line in open(tweetsfile, 'r'):     # read the whole file 
    #    tweets.append(json.loads(line))    # read the whole file 
    with open(tweetsfile, 'r') as file:     # read specific lines
        for i, line in enumerate(file):
            if (i>=start) and (i<=end):
                tweets.append(json.loads(line))
            elif (i>=end):
                break
    return tweets

def to_csv(lookup, tweets): # writes to outfile, always appending content
    #header = ['dataset', '.json', 'id', 'hashtag', 'class', 'content']
    #          dataset|jsonfile|tweets|tweets^lookup|lookup|tweets
    with open(outfile, 'a', encoding="utf-8", newline='') as file:
        writer = csv.writer(file)
        #writer.writerow(header)
        for tweet in tweets:
            hashtag = tweet['hashtags']
            if (hashtag is not None):
                hashtagXclass = from_lookup(lookup, hashtag)
                if (hashtagXclass is not None):
                    row = []
                    row.append(dataset)
                    row.append(jsonfile)
                    row.append(tweet['id'])
                    row.append(hashtag) # hashtag
                    row.append(hashtagXclass[1]) # class
                    row.append(tweet['content'])
                    writer.writerow(row)

# /////////////////// /////////////////// ///////////////////

lookup = load_lookup()

tweets = load_tweets(start=s, end=t)

#print(lookup) #debug
#print(from_lookup(lookup, 'FuraFilaDaVacinaNão')) # debug
#print(from_lookup(lookup, 'Shibalawaney'))        # debug
#print(from_lookup(lookup, 'BBB21'))               # debug

#print(tweets) # debug
#for tweet in tweets: # debug
#    print(f"ID: {tweet['id']}") # debug
#    print(f"CONTENT: {tweet['content']}") # debug
#    print(f"HASHTAGS: {tweet['hashtags']}") # debug
#    print("") # debug

to_csv(lookup, tweets)

#to_file(tweets) #debug

# /////////////////// /////////////////// ///////////////////
# Lookup table structure
# [('Hashtag1','Class1'), ('Hashtag2','Class2'), ..., ('HashtagN','ClassN')] 

# There are four collection data types in Python
# LIST          [ ]     ordered  , changeable. Allows duplicate members.
# TUPLE         ( )     ordered  , unchangeable. Allows duplicate members.
# SET           { }     unordered, unchangeable*, unindexed. No duplicate members.
# DICTIONARY    {:}     ordered**, changeable. No duplicate members.

# /////////////////// /////////////////// ///////////////////
