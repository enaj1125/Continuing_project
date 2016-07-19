# The goal of this program is to 1) Use Venmo payments that stream in to build a graph of users and their relationship with one another. 2) Calculate the median degree of a vertex in a graph and update this each time a new Venmo payment appears. Will be calculating the median degree across a 60-second sliding window.

try:                                                     # use json or the simplejson as a fallback.
    import json
except ImportError:
    import simplejson as json
from heapq import *
from datetime import *
import sys
    
class MedianFinder:  
    
    def __init__(self): # Intiitalize data structure
    
        self._heap = []
        self._dict = {}
        self._dict_node = {}
        self._small, self._large = [], []
        
    def prepare_streamData(self, each_item):     
        """ prepare streamData as time stamp and key pair """  
        time_stamp = datetime.strptime(each_item['created_time'], "%Y-%m-%dT%H:%M:%SZ")
        key = (each_item['target'], each_item['actor'])
        return key, time_stamp      
    
    def _push(self, item, if_large): # large = 1
        """ add an element in a heap, update the heap, and record the postion """
        if if_large:
            L = self._large
        else:
            L= self._small
        Dict = self._dict_node

        size = len(L)
        L[size:size] = [item]
        child_index, child = size, item
        parent_index = (child_index - 1) // 2
        parent = L[parent_index]

        while child < parent and parent_index >= 0:
            Dict[parent[1]] = (child_index, if_large) 
            L[parent_index], L[child_index] =  L[child_index], L[parent_index]
            child_index = parent_index
            child = L[child_index]
            parent_index = (child_index - 1) // 2
            parent = L[(child_index - 1) // 2]

        Dict[child[1]] = (child_index, if_large)

        
    def _delete(self, i, if_large):
        """ delete an element in a heap, update the heap, and record the postion """
        if if_large:
            L = self._large
        else: 
            L= self._small
        Dict = self._dict_node
        
        sizeL = len(L)
        if sizeL == 1:   # if only one element
            pop_item = L[0]
            del Dict[L[0][1]]
            L = L.pop()
            return pop_item

        pop_item = L[i] # save pop value
        
        # then delete it
        last = L[sizeL - 1]
        L[i] = last
        del L[-1]
        del Dict[pop_item[1]]
        
        parent_idx = i    
        child_idx = 2*i + 1
        
        if sizeL == 2:                          # special case L size == 2
            Dict[L[i-1][1]] = (0, if_large)
            return pop_item

        if child_idx >= sizeL - 1:              # deleted element has no child
            if i == sizeL - 1:                     # delete the not very last element       
                return pop_item
            else:                                  # delete the not very last element
                Dict[L[i][1]] = (i, if_large)
                return pop_item
        
        # Swap i's value with the smallest 
        while child_idx < sizeL-1:               # deleted element has child
            if child_idx + 1 < sizeL-1 and L[child_idx] > L[child_idx+1]:    
                child_idx += 1
                if L[parent_idx] < L[child_idx]:
                    break
            # swap with the smallest one            
            Dict[L[child_idx][1]] = (parent_idx ,if_large)
            L[child_idx], L[parent_idx] = L[parent_idx], L[child_idx]

            parent_idx = child_idx
            child_idx = 2*child_idx + 1 
        
        Dict[L[parent_idx][1]] = (parent_idx, if_large)        

        return pop_item
    
    
    def _add_heap_Node(self, item):   
        """ add an element in the heaps, while balancing the length of the two heaps """
        
        if not self._dict_node:                 # empty dict
            n = 0
        else:
            n = len(self._dict_node.keys())      
            
        ##################################
        ### if n is even, push into small; if n is odd, push into large
        if n%2 == 0:                            # even number             
            self._push((-item[0], item[1]), 0)  # push into small    (L, Dict, item, if_large)
            item = self._delete(0, 0)           # pop the smallest in large   (L, Dict, i, if_large):
            self._push((-item[0], item[1]), 1)  # push into big     
            
        else:   # odd number
            self._push(item, 1)          
            item = self._delete(0,1)         
            self._push((-item[0], item[1]), 0)     
      
            
        
    def _delete_heap_Node(self, item):  
       
        
        if not self._dict_node: # empty dict
            n = 0
        else:
            n = len(self._dict_node.keys())
        
        if_large = self._dict_node[item][1]
        i = self._dict_node[item][0]

        
        if if_large:   # delete from large
            self._delete(i, if_large)
            
            if n%2 == 0:
                item = self._delete(0, 0)
                self._push((-item[0], item[1]), 1) 
                
        else:    # delete from small
            self._delete(i, if_large)
            if n%2 >0:         # if odd number
                item = self._delete(0, 1)
                self._push((-item[0], item[1]), 0)
    
                
                
    
    def _add_node(self, node):
            
        """
        check if how the node should be added or updated
        """
        if not self._dict_node:                         # empty dict
            self._add_heap_Node((1, node))
        else:
            hash_keys = self._dict_node.keys() 
            if node not in hash_keys:                   # not exsit, add as new
                self._add_heap_Node((1, node))                 

            else:                                       # exsit, replace
                H_idx = self._dict_node[node][0]          # record the orginal value
                
                if self._dict_node[node][1]:            # if node stored in large      
                    H_value = self._large[H_idx][0] + 1 
                else:                                   # if node stored in small
                    H_value = -self._small[H_idx][0] + 1 
                
                
                # delete the node
                self._delete_heap_Node(node)
                
                # add as a new node
                self._add_heap_Node((H_value, node))
                
                
   
   

    def _delete_node(self, node):
        """
        check if how the node should be deleted
        """
        
        H_idx = self._dict_node[node][0]             # find the pos in heap
        
        if self._dict_node[node][1]:
            H_value = self._large[H_idx][0] - 1
            
        else:
            H_value = -self._small[H_idx][0] -1    # update the value
        
        
        # if updated value = 0: delete the node; else, replace the value
        
        self._delete_heap_Node(node)  # delete the node
        
        if H_value != 0:                           # update the node if its value > 0
            self._add_heap_Node((H_value, node))
            
    
        
    def check_timeWindow(self, each_item, current_time):  
        """
        check the 60s window and delete the old data based on current time.
        """
  
        while self._heap and (current_time - self._heap[0][0])/ timedelta(seconds=1) >= 60:  
            time_stamp, key = heappop(self._heap)
            
            if self._dict.get(key) == time_stamp:
                del self._dict[key]

                # delete the node from heap
                node1, node2 = key[0], key[1]
                self._delete_node(node1)
                self._delete_node(node2)
                

        
    def add_streamData(self, key, time_stamp, current_time):  
        
        if (time_stamp - current_time)/ timedelta(seconds=1) < 60:               
            
            if not self._dict.get(key, 0):              # if not exsiting, add to _dict, _dict_node
                node1, node2 = key[0], key[1]
                
                self._add_node(node1)
                self._add_node(node2)  
                
                self._dict[key] = time_stamp
               
            # update the dict and heap: if this is exsiting but with the older time stamp, 
            # not updating in the dict, but do add into heap
            else:
                if self._dict[key] <= time_stamp:
                    self._dict[key] = time_stamp 
                    
            heappush(self._heap, (time_stamp, key))          


    def find_Median(self):    
    # divide into small and large groups; get median  
        small, large = self._small, self._large
        
        if len(large) > len(small):
            return self._truncate(float(large[0][0]),2)
        return self._truncate((large[0][0] - small[0][0]) / 2.0, 2)
    
    def _truncate(self, f, n):
        # define a function for truncating a float f to n decimal places without rounding
        s = '%.12f' % f
        i, p, d = s.partition('.')
        return '.'.join([i, (d+'0'*n)[:n]])


    
# maintain two data structure: heap of stream data and heap of current edges
            
if __name__ == '__main__':                                      # make the file can be used as a module
    input_file, output_file = sys.argv[1], sys.argv[2]   # input 2 arguments

    mf = MedianFinder()
    with open(input_file) as inputs:    
        current_time = datetime.strptime('1970-01-01T00:00:00Z', "%Y-%m-%dT%H:%M:%SZ")
        median_list = []
        for line in inputs:
            try:
                
                each_item = json.loads(line.strip())   # transform json data (str) into dic data   
                key, time_stamp = mf.prepare_streamData(each_item) 
                if time_stamp > current_time:
                    current_time = time_stamp 

                mf.check_timeWindow(each_item, current_time)
                
                mf.add_streamData(key, time_stamp, current_time)

                median = mf.find_Median()
                print(median)
                median_list.append(median)
                
            except:# read in a line that is not in JSON format (sometimes error occured)
                continue

    # write output_list into a txt file
    file_output = open(output_file,"w")
    for x in median_list:
        file_output.write(str(x))
        file_output.write("\n")  
    file_output.close()       

        
