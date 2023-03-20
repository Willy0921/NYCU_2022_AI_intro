import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
    file = open(edgeFile)
    csvreader = csv.reader(file)

    path = []                   # Path found by DFS.
    dist = 0.0                  # The distance of the path.
    num_visited = 0             # The number of visited nodes in searching.

    stack = []                  # stack[]     : used in DFS process.
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
    stack.append(str_start)                 # Initially, add start node into stack.
    visited[str_start] = True
    while len(stack) > 0:                   # Use a while-loop and a stack to implement DFS.
        p = stack[-1]                       # Assign top elememt of stack to p.
        flg = 0                             # flg is to record whether p has unvisited adjacent node.
        if p == str_end:                    # Finish searching if p is the end node.
            break
        if have_adj.get(p, 0) == 0:         # Pop the top element from stack if p does not has adjacent node.
            stack.pop()                     
            continue
        for x in adj[p]:                    
            if not visited[x]:              # If x has not been visited, add it into stack
                stack.append(x)             # and set its previous node to p.
                num_visited += 1
                visited[x] = True
                prev[x] = p
                flg = 1
                break
        if flg:
            continue
        else:
            stack.pop()                     # Pop the top element of stack if all adjacent nodes of p are visited.
    
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
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
