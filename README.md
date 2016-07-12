# 
This program do:

- Use Venmo payments that stream in to build a  graph of users and their relationship with one another.

- Calculate the median degree of a vertex in a graph and update this each time a new Venmo payment appears. You will be calculating the median degree across a 60-second sliding window.


Developed by Yan Jiang using Python 3.

Use hash heap data structure to find median in incoming stream data.

1. This code use a data structure that combine the advantages of heap and hash table to m
        self._heap = []
        self._dict = {}
        self._dict_node = {}
        self._small, self._large = [], []

self._heap is used to iterate over the items in order of timestamp, which are provided by the heapq module.

self._dict is used to tell you wether a relationship of a pair of people  (key in hashtable) is known to the collection. For this, dict is a very good fit; just map the hash to the timestamp so you can look up each item easily using O[1].

self._small, self._large are used to use two heaps to keep counts of the degree of each node in the current time window. 

self._dict_node is used to store the name of node and its position in heap (self._small, self._large), so that we can look up each node easily with log(n).

 

2. How do I find the median of a dynamic changing collection of data?
I keep two heaps (or priority queues):
Max-heap small has the smaller half of the numbers.
Min-heap large has the larger half of the numbers.
This gives me direct access to the one or two middle values (they're the tops of the heaps), so getting the median takes O(1) time. And adding a number takes O(log n) time.

 
3. How to keep a rolling window of 60-s?
Use self._heap as an supplementry data to keep the timestamp is within the 60s window for self._dict. Meanwhile, update the two other data structures.
