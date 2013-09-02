#!/usr/bin/python

import sys
import copy


"""
    Data Structure
    Graph:
        {
            'A' : {
                    'B':[{'s':sif, 'e':eif, 'sip':sip, 'eip':eip, 'mt':mt},{},{}],
                    'C':[{},{}],
                    ......
                  }
        }

    Path:
        {
            'path' : [
                        {'A':[sif:sip]},{'B':[eif:eip, sif:sip]},{'D':[eif:eip]}   
                        ]
            'mt' : mt
        }

"""


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
            for p in vec_dict[e]:
                path_dict = {}
                path_dict['path'] = []
                path_dict['mt'] = p['mt']
                start = {}
                start[v0] = []
                start_small_dict = {}
                start_small_dict[p['s']] = p['sip']
                start[v0].append(start_small_dict)
                path_dict['path'].append(start)

                end = {}
                end[e] = []
                end_small_dict = {}
                end_small_dict[p['e']] = p['eip']
                end[e].append(end_small_dict)
                path_dict['path'].append(end)

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
        is_shortest = 1
        for spath in selected_list:
            if spath['path'][0].keys()[0] == v['path'][0].keys()[0] and spath['path'][-1].keys()[0] == v['path'][-1].keys()[0]:
                if v['mt'] > spath['mt']:
                    is_shortest = 0
                    obsoleted_list.append(v)
                    continue

        if is_shortest == 1:
            selected_list.append(v)

        v0 = v['path'][-1].keys()[0]
        #print "v0: %s" % v0
        A_list.append(v0)
        if v0 in B_list:
            B_list.remove(v0)

        vec_dict = g[v0]
        for e in vec_dict:
            if e not in A_list:
                for p in vec_dict[e]:
                    path_tmp = copy.deepcopy(v)  # must use deepcopy
                    start_small_dict = {}
                    start_small_dict[p['s']] = p['sip']
                    path_tmp['path'][-1].values()[0].append(start_small_dict)
                    end = {}
                    end[e] = []
                    end_small_dict = {}
                    end_small_dict[p['e']] = p['eip']
                    end[e].append(end_small_dict)
                    path_tmp['path'].append(end)
                    path_tmp['mt'] += p['mt']
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
            'B': {'C': [{'s':'1/2', 'e':'1/1', 'sip':'10.10.10.1', 'eip':'10.10.10.2', 'mt':40}], 'F': [{'s':'1/1', 'e':'1/2', 'sip':'10.10.15.2', 'eip':'10.10.15.1', 'mt': 100}]}, 
            'C': {'B': [{'s': '1/1', 'e':'1/2', 'sip':'10.10.10.2', 'eip':'10.10.10.1', 'mt':40}], 'D': [{'s':'1/2', 'e':'1/1', 'sip':'10.10.12.1', 'eip':'10.10.12.2', 'mt': 120}]}, 
            'D': {'C': [{'s': '1/1', 'e': '1/2', 'sip':'10.10.12.2', 'eip':'10.10.12.1', 'mt':120}], 'E': [{'s': '1/2', 'e': '1/1', 'sip':'10.10.13.1', 'eip':'10.10.13.2', 'mt': 40}]}, 
            'E': {'D': [{'s': '1/1', 'e': '1/2', 'sip':'10.10.13.2', 'eip':'10.10.13.1', 'mt':40}], 'F': [{'s': '1/2', 'e': '1/1', 'sip':'10.10.14.1', 'eip':'10.10.14.2', 'mt': 100}]}, 
            'F': {'B': [{'s':'1/2', 'e':'1/1', 'sip':'10.10.15.1', 'eip':'10.10.15.2', 'mt':100}], 'E': [{'s':'1/1', 'e':'1/2', 'sip':'10.10.14.2', 'eip':'10.10.14.1', 'mt': 100}]},
        }

    #print g

    path, ob = spf(g, 'B')

    import json
    print json.dumps(path)

