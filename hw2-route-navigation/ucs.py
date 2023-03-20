import csv
edgeFile = 'edges.csv'


def ucs(start, end):
    # Begin your code (Part 3)
    file = open(edgeFile)
    csvreader = csv.reader(file)

    path = []                   # Path found by UCS.
    dist = 0.0                  # The distance of the path.
    num_visited = 0             # The number of visited nodes in searching.

    set = {}                    # set[key]    : used to implement priority queue in UCS.
    d = {}                      # d[x]        : current minimum distance to start node for node x. 
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
    visited[str_start] = True
    d[str_start] = 0                        # Initially, set d[start] to 0, and update set[start].
    set[str_start] = d[str_start]           
    while len(set) > 0:                     # Use a while-loop and a priority queue to implement UCS.
        p = min(set, key=set.get)           # Get the node which has minimum set[node] from set and assign it to p.
        if not visited[p]:                  # If p is unvisited, then mark it as visited.
            visited[p] = True
            num_visited += 1
        if p == str_end:                    # Finish searching if p is the end node.
            break
        if have_adj.get(p, 0) == 0:         # Pop p from the priority queue if it does not has adjacent node.
            set.pop(p)                      
            continue
        for x in adj[p]:                    
            if d.get(x, 0) == 0 or d[p] + dis[p, x] < d[x]: # If d[x] does not have value or d[p] + dis[p, x] < d[x],
                d[x] = dis[p, x] + d[p]                     # then update d[x] with new minimum distance,
                prev[x] = p                                 # set x's previous node to p.
                set[x] = d[x]                               # and, add x into priority queue.
        set.pop(p)                          # Pop p from the priority queue 
    
    dist = d[str_end]                       # Assign d[end] to dist.
    path.append(end)                        # From end to start node, add prvious node into path.
    p = str_end                             
    while p != str_start:
        path.append(int(prev[p]))
        p = prev[p]
    path.reverse()                          # Reverse the list to let start node at the beginning of path.

    file.close()
    return path, dist, num_visited
    raise NotImplementedError("To be implemented")
    # End your code (Part 3)


if __name__ == '__main__':
    path, dist, num_visited = ucs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
