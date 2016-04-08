# InsightDataScience-Yan Jiang-cc

This is the solution of Yan Jiang to the coding challenge for the Insight Data Engineering Program implemented in "Python 3".

# Table of Contents
1. [Code Summary](README.md#code-summary)
2. [Details of Implementation](README.md#details-of-implementation)
3. [Building the Twitter Hashtag Graph](README.md#building-the-twitter-hashtag-graph)
4. [Modifying the Twitter Hashtag Graph with Incoming Tweet](README.md#modifying-the-twitter-hashtag-graph-with-incoming-tweet)
5. [Maintaining Data within the 60 Second Window](README.md#maintaining-data-within-the-60-second-window)


## Code Summary
This module package is developed by Yan Jiang in April, 2016. 

Task: The code is to calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears. You will thus be calculating the average degree over a 60-second sliding window.

Website of the code chanllenge:

The solution is based on: 
1) Read tweets data, convert into json object, and extract "created_at" and "hashtags" information.
2) Calculate the average degree of a vertex in a Twitter hashtag graph in a 60-s window.

How to represent and store edges and nodes?
The graph is storaged and maintained by a hashtable (dictionary in python). Each edge is represented as a key using a tuple, and the timing of the edge is stored in the value using a string.  

The logic of how to calculate the degree?
degree = total edges/total nodes

How to maintain a moving 60-s window?
If a edge appears multiple times, then its value in the dictionary is always updated into the most current one.
Thus, the moving 60-s window is maintained by using the most recent tweet and find its previous 60-s window.


## Packages used/Dependencies
datetime
https://docs.python.org/3/library/datetime.html

json/simplejson
https://pypi.python.org/pypi/simplejson/

sys
https://docs.python.org/3.0/library/sys.html

## trade-off of design

1. compare dictionary vs list storage
2. compare store edges using 1 or 2 tuple

dictionary VS list

store two edge vs one

other possible ways

## Test cases
 
Test case 1
2-tweets, all distinct nodes


Test case 2
1-tweets, 1 hashtag
This test is created for testing:
What should the average be if the graph has no connections 
(e.g. if the first tweet doesn't have at least two hashtags)?
If there are no connections for the entire graph, then you can count the average as 0.00.

expect output: 0.00

Test case 3
name: tweets_10_test
1-tweets, 5 hashtag 

expect output: 4.00

Test case 4
name: tweets_30_test
3-tweets, overlapping

expect: 30/7 = 4.28
4.00, 4.85, 5.63

Test case 5
insight example: 9 tweets

## How to run the program



