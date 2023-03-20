import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    file1 = open(edgeFile)
    file2 = open(heuristicFile)
    csvreader1 = csv.reader(file1)
    csvreader2 = csv.reader(file2)

    path = []                     # Path found by A*.
    dist = 0.0                    # The distance of the path.
    num_visited = 0               # The number of visited nodes in searching.

    set = {}                      # set[key]          : used to implement priority queue in A*.
    d = {}                        # d[x]              : current minimum distance to start node for node x. 
    adj = {}                      # adj[x][]          : stores adjacent nodes for node x.
    dis = {}                      # dis[x, y]         : distance between node x and y.
    dis_To_Goal = {}              # dis_To_Goal[x, y] : Euclidean distance from node x to y.
    visited = {}                  # visited[x]        : records whether a node x is visited.
    have_adj = {}                 # have_adj[x]       : records whether a node x has adjacent nodes.
    prev = {}                     # prev[x]           : records previous passing node x of each node.

    title = 1
    prev_id = ''
    for row in csvreader1:        # Load data from edges.csv with csvreader1 and a for-loop.
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
    
    title = 1
    for row in csvreader2:        # Load data from heuristic.csv with csvreader2 and a for-loop.
        if title:
            goal1 = row[1]
            goal2 = row[2]
            goal3 = row[3]
            title = 0
            continue
        dis_To_Goal[row[0]] = {}
        dis_To_Goal[row[0]][goal1] = float(row[1])
        dis_To_Goal[row[0]][goal2] = float(row[2])
        dis_To_Goal[row[0]][goal3] = float(row[3])

    str_start = str(start)
    str_end = str(end)
    visited[str_start] = True
    d[str_start] = 0                        # Initially, set d[start] to 0, and update set[start].
    set[str_start] = d[str_start]           
    while len(set) > 0:                     # Use a while-loop and a priority queue to implement A*.
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
                prev[x] = p                                 # set x's previous node to p,
                set[x] = d[x] + dis_To_Goal[x][str_end]     # and update set[x] with d[x] + dis_To_Goal[x][str_end].
        set.pop(p)                          # Pop p from the priority queue.

    dist = d[str_end]                       # Assign d[end] to dist.
    path.append(end)                        # From end to start node, add prvious node into path. 
    p = str_end                             
    while p != str_start:
        path.append(int(prev[p]))
        p = prev[p]
    path.reverse()                          # Reverse the list to let start node at the beginning of path.

    file1.close()
    file2.close()
    return path, dist, num_visited
    raise NotImplementedError("To be implemented")
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
