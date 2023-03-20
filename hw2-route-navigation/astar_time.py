import csv
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    file1 = open(edgeFile)
    csvreader1 = csv.reader(file1)
    file2 = open(heuristicFile)
    csvreader2 = csv.reader(file2)

    path = []                      # Path found by A*(time).
    time = 0.0                     # The time of the path.
    num_visited = 0                # The number of visited nodes in searching.

    set = {}                       # set[key]          : used to implement priority queue in A*.
    pass_time = {}                 # pass_time[x]      : current minimum time from start node to node x. 
    adj = {}                       # adj[x][]          : stores adjacent nodes for node x.
    dis = {}                       # dis[x, y]         : distance between node x and y.
    speed = {}                     # speed[x, y]       : speed limit between node x and y.
    dis_To_Goal = {}               # dis_To_Goal[x, y] : Euclidean distance from node x to y.
    visited = {}                   # visited[x]        : records whether a node x is visited.
    have_adj = {}                  # have_adj[x]       : records whether a node x has adjacent nodes.
    prev = {}                      # prev[x]           : records previous passing node x of each node.
    max_speed = 0.0                # Records max speed limit from heuristic.csv.

    title = 1
    prev_id = ''
    for row in csvreader1:         # Load data from edges.csv with csvreader1 and a for-loop.
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
        speed[row[0], row[1]] = float(row[3]) * 5/18
        if speed[row[0], row[1]] > max_speed:
            max_speed = speed[row[0], row[1]]
        adj[row[0]].append(row[1])
        
    title = 1
    for row in csvreader2:         # Load data from heuristic.csv with csvreader2 and a for-loop.
        if title:
            goal1 = row[1]
            goal2 = row[2]
            goal3 = row[3]
            title = 0
            continue
        dis_To_Goal[row[0]] = {}
        dis_To_Goal[row[0], goal1] = float(row[1])
        dis_To_Goal[row[0], goal2] = float(row[2])
        dis_To_Goal[row[0], goal3] = float(row[3])

    str_start = str(start)
    str_end = str(end)    
    visited[str_start] = True
    pass_time[str_start] = 0                # Initially, set pass_time[start] to 0, and update set[start].
    set[str_start] = pass_time[str_start]
    while len(set) > 0:                     # Use a while-loop and a priority queue to implement A*(time).
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
            '''
            I change the heuristic function with 'min time to the end' (distance to end / max speed limit) in this part.
            If pass_time[x] does not have value or pass_time[p] + (dis[p, x] / speed[p, x]) < pass_time[x],
            then update pass_time[x] with new minimum time, set x's previous node to p,
            and update set[x] with pass_time[x] + (dis_To_Goal[x, str_end] / max_speed).
            '''
            if pass_time.get(x, 0) == 0 or pass_time[p] + (dis[p, x] / speed[p, x]) < pass_time[x]:
                pass_time[x] = (dis[p, x] / speed[p, x]) + pass_time[p]
                prev[x] = p
                set[x] =  pass_time[x] + (dis_To_Goal[x, str_end] / max_speed)
        set.pop(p)                          # Pop p from the priority queue.
    
    time = pass_time[str_end]               # Assign pass_time[end] to time.
    path.append(end)                        # From end to start node, add prvious node into path. 
    p = str_end
    while p != str_start:
        path.append(int(prev[p]))
        p = prev[p]
    path.reverse()                          # Reverse the list to let start node at the beginning of path.

    file1.close()
    file2.close()
    return path, time, num_visited
    raise NotImplementedError("To be implemented")
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
