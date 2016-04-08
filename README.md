# InsightDataScience-Yan Jiang-cc

This is the solution module to the coding challenge for the 2016 Insight Data Engineering Program implemented in "Python 3".
Developed by Yan Jiang, April, 2016

Website of the code chanllenge: https://github.com/InsightDataScience/coding-challenge

# Table of Contents
1. [Overview of the Coding Challenge Solution](README.md#code-summary)
2. [Dependencies/Modules](README.md#Dependencies/Modules)
3. [Technical Design and Trade-off](README.md#Technical-Design-and-Trade-off)
4. [Mathematical Way to Calculate the Rolling Degree](README.md#mathematical-Way-to-Calculate-the-Rolling-Degree)
5. [Test Cases](README.md#test-cases)
6. [How to Run the Program](README.md#how-to-run-the-program)


## Overview of the Coding Challenge Solution

The task is to calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears. You will thus be calculating the average degree over a 60-second exclusive sliding window.

The solution were implemented in two major steps: 

1) Read tweets data, convert into json object, and extract "created_at" and "hashtags" information.

2) Store and update Twitter data in a hash table (dictionary), calculate the average degree of a vertex in a Twitter hashtag graph in a 60-s window.

##### How to represent graph and keep track of the edges and nodes?

The graph is stored and maintained by a dictionary (hash table). Each pair of edges is represented as the "key" using a tuple, and the timing of this pair of edges is stored as the "value" using a string.  

##### How to maintain a moving 60-s window?

If an edge appears multiple times in the 60-s window, then its timing would be always updated to the most recent timing in the dictionary. 
Thus, the graph should only consist of tweets that arrived in the last 60 seconds as compared to the maximum timestamp that has been processed.

##### The logic of calculating the rolling degree?

By counting all the current updated edges and nodes, the average degree could be calculated as:

> degree = total edges / total nodes


## Dependencies/Modules
There are three modules need to be imported, and they can be downloaded from:

1) datetime
https://docs.python.org/3/library/datetime.html

2) json or simplejson
https://pypi.python.org/pypi/simplejson/

3) sys
https://docs.python.org/3.0/library/sys.html

## Technical Design and Trade-off
#####1). Data structure and Time complexity

The graph (edges, nodes) can be maintained using either the dictionary or list. Since the time complexity of search, insert, delete is O(1) for the dictionary, while o(n) for a list. Therefore, the dictionary is more efficient and was selected to do the job. 

#####2). Data Storage Memory VS. Time Complexity (in the context of big input data )

If two nodes a, b were connected, the resulting edges can be represented using two tuples (a,b) and (b,a). Or they could be represented by one tuple (a, b).

Using two tuples would consume more data storage memory, but later when search if one specific edge (e.g, (a,b)) has been existing in the graph it only need to search once ( search (a,b). 

While, using one tuple would save data storage memory by reducing the graph edges to half, but each time when search if an edge is existing in the graph (e.g,(a,b) ) it would need search twice (search if (a,b) or (b,a) is existing ). 

However, since the FAQ of the code challenge indicates the program should have the ability of dealing with large input datasets, and the time complexity of search operation is O(1) for hash table, which is not a big add-on if search one more time. Therefore, here I choose give priority to saving memory for big input data concern. 


## Alternative (Mathematical) Way to Calculate the Rolling Degree

> current edges = previous edges + new edges - overlapping edges

> current nodes = previous nodes + new nodes - overlapping nodes

in which, the new edges = number of new nodes * (number of new nodes - 1)

Thus, the degree can be calculated by keep tracking five variables: current edges, current nodes, new nodes, overlapping nodes, overlapping edges. 

This method is more complicated, but provides a more mathematical way to describe how the new edges are formed by keeping tracking the overlapping hashtags.  



## Test Cases
Five test cases were used to test this solution:

#####Test case 1: (provided by the official website)

name: test-1-tweets-all-distinct

feature: 2-tweets, all distinct nodes


#####Test case 2: (Yan Jiang created)

name: test-2-tweets-one-hashtag

feature: 1-tweets, 1 hashtag

This test is created for testing: What should the average be if the graph has no connections (e.g. if the first tweet doesn't have at least two hashtags)?
If there are no connections for the entire graph, then you can count the average as 0.00.

expect output: 0.00

#####Test case 3: (Yan Jiang created)

name: test-3-ten-tweets

feature: 1 effective tweets, 5 hashtag 

This test is created for testing the first part of code : initializing the dictionary using the first tweet.
expect output: 4.00

#####Test case 4: (Yan Jiang created)

name: test-4-30-tweets

feature: 3 effective tweets, overlapping

This test is created for testing the rolling tweets that overlapping hashtags 

expect output: 4.00, 4.85, 5.63

#####Test case 5: (Yan Jiang created)

name: test-5-10k-tweets

This test is created for testing the efficiency of the program to process large (relatively) input data. 

expect output: which I calculated using another method -- the mathematical method discussed above.

## How to Run the Program

I format and organize the program based on the required "Repo directory structure".

To run the average_degree.py using the run.sh script: 

```
submission$ sh run.sh
```

To test the program: 

```
insight_testsuite$ sh run_tests.sh 
```
The structure of this submission includes: 
```
├── README.md 
├── run.sh
├── src
│   └── average_degree.java
├── tweet_input
│   └── tweets.txt
├── tweet_output
│   └── output.txt
└── insight_testsuite
    ├── run_tests.sh
    └── tests
        └── test-2-tweets-all-distinct
        │   ├── tweet_input
        │   │   └── tweets.txt
        │   └── tweet_output
        │       └── output.txt
        └── test-2-tweets-one-hashtag
        │    ├── tweet_input
        │    │   └── tweets.txt
        │    └── tweet_output
        │        └── output.txt
        ── test-3-ten-tweets
        │    ├── tweet_input
        │    │   └── tweets.txt
        │    └── tweet_output
        │        └── output.txt
        ── test-4-30-tweet
        │    ├── tweet_input
        │    │   └── tweets.txt
        │    └── tweet_output
        │        └── output.txt
        ── test-5-10k-tweet
            ├── tweet_input
            │   └── tweets.txt
            └── tweet_output
                └── output.txt
```
