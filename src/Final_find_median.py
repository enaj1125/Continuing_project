# maintain two data structure: heap of stream data and heap of current edges

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
        # prepare streamData as time stamp and key pair   
        time_stamp = datetime.strptime(each_item['created_time'], "%Y-%m-%dT%H:%M:%SZ")
        key = (each_item['target'], each_item['actor'])
        return key, time_stamp      
    
    def _push(self, item, if_large): 

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
        # then delte it
        last = L[sizeL - 1]
        L[i] = last
        del L[-1]
        del Dict[pop_item[1]]
        
        parent_idx = i    
        child_idx = 2*i + 1

        # Swap i's value with the smallest 
        while child_idx < sizeL-1:         
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

        if not self._dict_node: # empty dict
            n = 0
        else:
            n = len(self._dict_node.keys())                
        ##################################
        ### if n is even, push into small; if n is odd, push into large
        if n%2 == 0:     # even number             
            self._push((-item[0], item[1]), 0)  # push into small    (L, Dict, item, if_large)
            item = self._delete(0, 0)           # pop the smallest in large   (L, Dict, i, if_large):
            self._push((-item[0], item[1]), 1)  # push into big              
        else:   # ood number
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
            if n%2 ==0:
                item = self._delete(0, 0)
                self._push((-item[0], item[1]), 1) 
                
        else:    # delete from small
            self._delete(i, if_large)
            if n%2 >0:
                item = self._delete(0, 1)
                self._push((-item[0], item[1]), 0)
                
    
    def _add_node(self, node):             
        """
        check if how the node should be added or updated
        """
        if not self._dict_node: # empty dict
            self._add_heap_Node((1, node))
        else:
            hash_keys = self._dict_node.keys() 
            if node not in hash_keys: # not exsit, add as new
                self._add_heap_Node((1, node))                 

            else:                                         # exsit, replace
                H_idx = self._dict_node[node][0]  # record the orginal value
                
                if self._dict_node[node][1]:   # if node stored in large      
                    H_value = self._large[H_idx][0] + 1 # update the value
                else:
                    H_value = -self._small[H_idx][0] + 1 # update the value
                
                # delete the node
                self._delete_heap_Node(node)
                
                # add as a new node
                self._add_heap_Node((H_value, node))
                
                
    def add_streamData(self, key, time_stamp, current_time):  
   
        # check if a pair not exsit, then push into 
        if not self._dict.get(key, 0):
            node1, node2 = key[0], key[1]
            self._add_node(node1)
            self._add_node(node2)         
               
        ###################### update the #########
        self._dict[key] = time_stamp
        heappush(self._heap, (time_stamp, key))     
   

    def _delete_node(self, node):
        H_idx = self._dict_node[node]            # record the orginal value
        H_value = self._heap_node[H_idx][0] - 1   # update the value
        
        # if updated value = 0: delete the node; else, replace the value
        delete_heap_Node(self._heap_node, H_idx)
        
        if H_value > 0: 
            add_heap_Node(self._heap_node, (H_value, node1))
            
    
        
    def check_timeWindow(self, each_item, current_time):  
        # check the 60s window
        # check if the current time is newer than current time 
            
        while self._heap and (current_time - self._heap[0][0])/ timedelta(seconds=1) >= 60:
            time_stamp, key = heappop(self._heap)
            if self._dict.get(key) == time_stamp:
                del self._dict[key]
                # delete the node from heap
                node1, node2 = key[0], key[1]
                self._delete_node(node1)
                self._delete_node(node2)

        

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

                mf.add_streamData(key, time_stamp, current_time)

                mf.check_timeWindow(each_item, current_time)

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
