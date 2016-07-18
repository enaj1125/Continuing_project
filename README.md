# Hash-heap data structure for computing the median of a stream data

####### Developed by Yan Jiang using Python 3.

## Overview
The goal of this program is to 1) Use Venmo payments that stream in to build a graph of users and their relationship with one another. 2) Calculate the median degree of a vertex in a graph and update this each time a new Venmo payment appears. You will be calculating the median degree across a 60-second sliding window.

## Highlights

### Data structure
Heap is an ideal data structure for maintaining a dynamically changing stream data; while hashtable is fast in search an element. This program create a data structure that combine the advantages of heap and hash table:

   self._heap = []

..self._dict = {}

...self._dict_node = {}

...self._small, self._large = [], []

This data structure use two pairs of hash-heap structures. The first pair (self._heap, self._dict) is used for storing the edges and maintain a rolling 60-s window. When each new payment data comes in, self._dict is used to check whether a relationship of a edge  (key in hashtable) is exsiting in the 60s-s collection and store the data. For this, dict is a very good fit; just map the hash to the timestamp so you can look up each item easily using O[1]. While self._heap serves as a supplementary data structure and is used to iterate over the items and pop out the payment data that is older than 60s, and the self._dict will also be updated at the same time. 

In hash table, the average time complexcity of search, insertion, deletion is O(1). In heap, the time complexcity of insertion (push), deletion(pop) is log(n). So the time complexicity is log(n). 

The second pair(self._small, sel._large, self._dict_node) is used for sotring the nodes and the corresponding degree. The self._dict_node is used for storing each node and its position in the two heap structures. So that the heaps can find any element in O(1), and delete the element while reheapify in log(n).   self._small, self._large are used to use two heaps to keep tracking each node and the degree of them in the current time window collection. 

When each new node is added in, it is added in the heaps () and the corresponding postion would be updated and stored in the self._dict_node. Takes log(n).

 
### How to find the median of a dynamic changing stream of data?
I keep two heaps (or priority queues):
Max-heap small has the smaller half of the numbers.
Min-heap large has the larger half of the numbers (all numbers were make negative values)
This gives direct access to the one or two middle values (they're the tops of the heaps), so getting the median takes O(1) time. And adding or deleting a number takes O(log n) time.

The advantage of using two heaps is that no need to sort all the numbers in the collection.

 
