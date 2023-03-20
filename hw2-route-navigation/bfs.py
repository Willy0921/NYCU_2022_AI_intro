import csv
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
    file = open(edgeFile)
    csvreader = csv.reader(file)

    path = []                   # Path found by BFS.
    dist = 0.0                  # The distance of the path.
    num_visited = -1            # The number of visited nodes in searching.

    queue = []                  # queue[]     : used in BFS process.
    adj = {}                    # adj[x][]    : stores adjacent nodes for node x.
    dis = {}                    # dis[x, y]   : distance between node x and y.
    visited = {}                # visited[x]  : records whether a node x is visited.
    have_adj = {}               # have_adj[x] : records whether a node x has adjacent nodes.
    prev = {}                   # prev[x]     : records previous passing node x of each node.
                  
    title = 1                               
    prev_id = ''                            
    for row in csvreader:       # Load data from edges.csv with csvreader and a for-loop.
        if title:                           
            title = 0                       
            continue                        
        if row[0] != prev_id:               
            prev_id = row[0]                
            adj[row[0]] = []                
            have_adj[row[0]] = True         
            visited[row[0]] = False         
        visited[row[1]] = False             
        dis[row[0], row[1]] = float(row[2]) 
        adj[row[0]].append(row[1])          

    str_start = str(start)                  
    str_end = str(end)                      
    queue.append(str_start)                 # Initially, add start node into queue.
    visited[str_start] = True
    while len(queue) > 0:                   # Use a while-loop and a queue to implement BFS.
        p = queue.pop(0)                    # Pop the first element from queue and assign it to p per time.
        num_visited += 1         
        if p == str_end:                    # Finish searching if p is the end node.
            break
        if have_adj.get(p, 0) == 0:         # Determine whether p has adjacent node.
            continue
        for x in adj[p]:                   
            if not visited[x]:              # If x has not been visited, add it into queue
                queue.append(x)             # and set its previous node to p.
                visited[x] = True
                prev[x] = p
    
    path.append(end)                        # From end to start node, add prvious node into path,
    p = str_end                             # and sum up their distance.
    while p != str_start:                   
        path.append(int(prev[p]))
        dist += dis[prev[p], p]
        p = prev[p] 
    path.reverse()                          # Reverse the list to let start node at the beginning of path.

    file.close()
    return path, dist, num_visited
    raise NotImplementedError("To be implemented")
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
