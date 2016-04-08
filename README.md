# InsightDataScience-Yan Jiang-cc

This is the solution of Yan Jiang to the coding challenge for the Insight Data Engineering Program implemented in "Python 3".

# Table of Contents
1. [Code Summary](README.md#code-summary)
2. [Details of Implementation](README.md#details-of-implementation)
3. [Building the Twitter Hashtag Graph](README.md#building-the-twitter-hashtag-graph)
4. [Modifying the Twitter Hashtag Graph with Incoming Tweet](README.md#modifying-the-twitter-hashtag-graph-with-incoming-tweet)
5. [Maintaining Data within the 60 Second Window](README.md#maintaining-data-within-the-60-second-window)


## Code Summary
This package is developed by Yan Jiang in April, 2016. 
The code is to calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears. You will thus be calculating the average degree over a 60-second sliding window.

The solution is based on

## features 
# the logic of how to calculate the degree?

how to represent and store edges and nodes
1. compare dictionary vs list storage
2. compare store edges using 1 or 2 tuple

how to represent a moving window?



## Packages used/Dependencies
While you may use publicly available packages, 
modules, or libraries, you must document any dependencies in your accompanying README file.



## trade-off of design
dictionary VS list
store two edge vs one

1. other possible ways

## test cases
 
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
