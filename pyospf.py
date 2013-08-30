#!/usr/bin/python

import sys
import copy


def spf(g, v):
    A_list = []
    B_list = []

    if v in g:
        A_list.append(v)
    else:
        raise ValueError("Not found")

    for k in g:
        if k != v:
            B_list.append(k)

    """
    # debug
    print "A list: %s" % A_list
    print "B list: %s" % B_list
    """

    selected_list = []
    waited_list = []
    obsoleted_list = []
    
    v0 = A_list[-1]
    vec_dict = g[v0]
    for e in vec_dict:
        if e not in A_list:
            path_dict = {}
            path_dict['path'] = []
            path_dict['mt'] = vec_dict[e]
            path_dict['path'].append(v0)
            path_dict['path'].append(e)
            waited_list.append(path_dict)

    """
    print "!!!!!!!!!!"
    print "A : %s" % str(A_list)
    print "B : %s" % str(B_list)
    print "selected: %s" % str(selected_list)
    print "waited: %s" % str(waited_list)
    print "!!!!!!!!!!"
    """

    #while len(B_list) > 0 or len(waited_list) > 0:
    while len(waited_list) > 0:
        mt = sys.maxint
        v = {}
        ix = -1
        for item in waited_list:
            if item['mt'] < mt:
                mt = item['mt']
                v = item

        waited_list.remove(v)

        # shortest path
        for spath in selected_list:
            if spath['path'][0] == v['path'][0] and spath['path'][-1] == v['path'][-1]:
                if v['mt'] > spath['mt']:
                    obsoleted_list.append(v)
                    continue

        selected_list.append(v)

        v0 = v['path'][-1]
        #print "v0: %s" % v0
        A_list.append(v0)
        if v0 in B_list:
            B_list.remove(v0)

        vec_dict = g[v0]
        for e in vec_dict:
            if e not in A_list:
                path_tmp = copy.deepcopy(v)  # must use deepcopy
                path_tmp['path'].append(e)
                path_tmp['mt'] += vec_dict[e]
                waited_list.append(path_tmp)

        """
        print "!!!!!!!!!!"
        print "A : %s" % str(A_list)
        print "B : %s" % str(B_list)
        print "selected: %s" % str(selected_list)
        print "waited: %s" % str(waited_list)
        print "!!!!!!!!!!"
        """

    return (selected_list, obsoleted_list)


if __name__ == "__main__":
    g = {   
            'A':{'B':10},
            'B': {'C': 40, 'F': 100}, 
            'C': {'B': 40, 'D': 120}, 
            'D': {'C': 120, 'E': 40}, 
            'E': {'D': 40, 'F': 100, 'G':10}, 
            'F': {'B': 100, 'E': 100},
            'G': {'E':10},
        }

    #print g

    path, ob = spf(g, 'A')

    import json
    print json.dumps(path)

