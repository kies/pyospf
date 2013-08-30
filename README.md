pyospf
======
Calc the shortest path use OSPF algorithm.


Data Structure
INPUT:
    Graph
    {
        'A' : {
                'B':[{'s':sif, 'e':eif, 'mt':mt},{},{}],
                'C':[{},{}],
                ......
              }
    }

OUTPUT:
    Path
    {
        'path' : [
                    {'A':[sif, eif]},{'B':[sif, eif]},{'D':[sif,eif]}   
                    ]
        'mt' : mt
    }
