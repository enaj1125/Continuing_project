
# Import libraries

import sys
from datetime import datetime
try:                                                     # use json or the simplejson as a fallback.
    import json
except ImportError:
    import simplejson as json
    


def get_average_degree(input_tweets_file):
    ##########################################################################
    ### 1. Read tweets data, convert into json object, and extract "created_at" and "hashtags" information   
    tweets_filename = input_tweets_file
    tweets_file = open(tweets_filename, "r")
    tweets_list = []
    
    for line in tweets_file:
        try:
            # Read in one line each time, convert it into a json object. 
            # for simplicity assume that all the tweets contain at least one word.
            tweet = json.loads(line.strip())
            if 'text' in tweet:                                # only messages contains 'text' field (at least one word) is a tweet 
                hashtags = []
                for hashtag in tweet['entities']['hashtags']:  # use the hashtags directly from the entity field of the JSON
                    hashtags.append(hashtag['text'])
            
                if hashtags:                                   # get rid of empty hashtags
                    tweets_list.append([tweet['created_at'], hashtags])

        except:
            # read in a line that is not in JSON format (sometimes error occured)
            continue
            
    def truncate(f, n):
        # define a function for truncating a float f to n decimal places without rounding
        s = '%.12f' % f
        i, p, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])
        
    ###########################################################################
    ### 2. Calculate the average degree of a vertex in a Twitter hashtag graph in a 60-s window
    degree_list = []
    first_raw_tweet = tweets_list[0][1]
    first_tweet = list(set(first_raw_tweet))    # deal with case when if a hashtag appears multiple times in a tweet

    
    # 1). There is only one tweet
    if len(tweets_list) == 1:                 # zero or one hashtag
        if len(first_tweet) < 2:
            return ['0.00']
        else:                                 # at least two hashtags
            # return the degree directly
            degree_list.append(truncate(len(first_tweet) - 1, 2))
            return degree_list
    
    # 2). There is more than one tweets
    start_t_time = tweets_list[0][0][4:19] + tweets_list[0][0][25:]
    d1 = datetime.strptime(start_t_time, '%b %d %H:%M:%S %Y')       
    
    # build a tweets dictionary to store the graph, initialize the key and values of the 1st tweet
    tweets_dict = {}          
    for p in range(0, len(first_tweet)):
        for q in range(p+1, len(first_tweet)):
            tweets_dict[(first_tweet[p], first_tweet[q])] = d1
    degree_list.append(truncate(len(first_tweet) - 1, 2))
    
    # Loop through each coming new tweet and calculate the average degree
    i = 1
    
    while i < len(tweets_list):
        # 1]. Get the new tweet and calculate the time diff between nth and (n+1)th tweet
        next_raw_tweet = tweets_list[i][1]
        next_tweet = list(set(next_raw_tweet))
        next_tweet_t = tweets_list[i][0][4:19] + tweets_list[i][0][25:]
        d2 = datetime.strptime(next_tweet_t, '%b %d %H:%M:%S %Y')
        diff = (d2 - d1).total_seconds()
    
        # 2]. Update the graph based on a 60-s window: 
        # for tweets contain hashtag less than two, still process it but not contribute to the graph
        if diff <= - 60: 
            # if it falls out of order and very old(>60s), ignore it in time window, rolling degree remain the same
            degree = degree  # degree remain the same
        
        else:  # including abs(diff) < 60 & diff >= 60
            # a. update the time window
            d1 = max(d1, d2) 

            # b. check if current tweets in dict are in the time window
            for key, value in list(tweets_dict.items()):         
                if ((d1 - value).total_seconds()) >= 60:
                    del tweets_dict[key]
       
            # c. if len of hashtags > 2, add n+1 tweet to the collection and update the time to the latest time     
            if len(next_tweet) > 1:  
                # add elements in the (n+1)th tweets to the collection and update the time to the latest
                for p in range(0, len(next_tweet)):
                    for q in range(p+1, len(next_tweet)):                   
                        pair1, pair2 = (next_tweet[p], next_tweet[q]), (next_tweet[q], next_tweet[p])  
                        if tweets_dict.get(pair1, 0):
                            tweets_dict[pair1] = max(d2, tweets_dict.get(pair1, d2))
                        else:
                            tweets_dict[pair2] = max(d2, tweets_dict.get(pair2, d2))

                        # update the time window
                        d1 = max(d2, d1)

            # d. calculate and output a degree         
            edges = list(tweets_dict.keys())
            nodes = set([x[0] for x in edges] + [x[1] for x in edges])  # turn a list of tuples into lists, get unique values
            total_edges = len(edges) * 2
            total_nodes = len(nodes)
        
            if total_nodes:
                degree = truncate(total_edges/total_nodes, 2)           # precision: 2-digits after decimal place with truncation
            else:
                degree = truncate(0, 2)
            
        # 3]. Finally, update the i
        i = i + 1
        degree_list.append(degree)
            

    return degree_list


if __name__ == '__main__':                                      # make the file can be used as a module
    input_tweets_file, output_file = sys.argv[1], sys.argv[2]   # input 2 arguments
    output_list = get_average_degree(input_tweets_file) 
    
    # write output_list into a txt file
    file_output = open(output_file,"w")
    for x in output_list:
        file_output.write(str(x))
        file_output.write("\n")  
    file_output.close()
