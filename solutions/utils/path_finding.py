import heapq


class Node:

    def __init__(self, state, cost_to_here: float = 0, prev_node=None):
        self.state = state
        self.cost_to_here = cost_to_here
        self.prev_node = prev_node

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.cost_to_here < other.cost_to_here

    def __hash__(self):
        return hash(self.state)


class PathFinder:
    def __init__(self):
        raise NotImplementedError()

    def outgoing_edges(self, node):
        raise NotImplementedError()

    def estimate_cost_to_goal(self, from_node):
        raise NotImplementedError()

    def find_path(self, start_node: Node):

        visited = set()  # Set of nodes that are already visited

        path_queue = []

        heapq.heappush(path_queue, (0, start_node))

        while path_queue:
            _, node = heapq.heappop(path_queue)

            if node in visited:
                continue
            if self.estimate_cost_to_goal(node) == 0:
                return node.cost_to_here, reconstruct_path(node)
            else:
                visited.add(node)

            for neighbour in self.outgoing_edges(node):

                future_cost = self.estimate_cost_to_goal(node)
                total_cost_estimate = node.cost_to_here + future_cost

                heapq.heappush(path_queue, (total_cost_estimate, neighbour))

        return -1, []

    def find_all_paths(self, start_node: Node):

        optimal_paths = []

        optimal_path_cost = None

        visited = {}  # Dictonary of visited nodes and the optimal cost to get there

        path_queue = []

        heapq.heappush(path_queue, (0, start_node))

        while path_queue:
            _, node = heapq.heappop(path_queue)

            if self.estimate_cost_to_goal(node) == 0:
                if not optimal_path_cost:
                    optimal_path_cost = node.cost_to_here

                if node.cost_to_here == optimal_path_cost:
                    path = reconstruct_path(node)
                    optimal_paths.append(path)
                else:
                    break

            elif node in visited and visited[node] < node.cost_to_here:
                continue
            else:
                visited[node] = node.cost_to_here

            for neighbour in self.outgoing_edges(node):

                future_cost = self.estimate_cost_to_goal(node)
                total_cost_estimate = node.cost_to_here + future_cost

                heapq.heappush(path_queue, (total_cost_estimate, neighbour))

        return optimal_path_cost, optimal_paths


def reconstruct_path(node: Node):
    path = []

    while node:
        path.append(node.state)
        node = node.prev_node

    return list(reversed(path))
