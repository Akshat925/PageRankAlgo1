from collections import defaultdict
out_degrees = []
num_pages = 0

def I(h, a, importance):
    a = [0.0] * len(h)
    b = 0.0
    c = 0.0

    for i in range(len(h)):
        if len(h[i]) == 0:
            a[i] = 0
        else:
            for j in range(len(h[i])):
                destination, weight = h[i][j]
                a[i] += weight * importance[destination]
            a[i] *= 0.85

    for i in range(len(h)):
        if out_degrees[i] != 0:
            b += a[i] * importance[i]
            c += importance[i]

    b *= 0.85
    c = c * 0.15 / num_pages

    b_vec = [b if out_degrees[i] != 0 else 0.0 for i in range(len(h))]
    c_vec = [c if out_degrees[i] != 0 else 0.0 for i in range(len(h))]

    for i in range(len(importance)):
        importance[i] = a[i] + b_vec[i] + c_vec[i]

def G(h_matrix, a_matrix, edges, node_degrees):
    global num_pages
    for edge in edges:
        source, destination = edge
        h_matrix[destination].append((source, 1.0))
        node_degrees[source] += 1
        out_degrees[source] += 1
        out_degrees[destination] += 1

    for i in range(len(h_matrix)):
        if out_degrees[i] != 0:
            num_pages += 1

    for i in range(len(h_matrix)):
        for j in range(len(h_matrix[i])):
            h_matrix[i][j] = (h_matrix[i][j][0], 1.0 / node_degrees[h_matrix[i][j][0]])

    for i in range(len(node_degrees)):
        if node_degrees[i] == 0 and out_degrees[i] != 0:
            a_matrix[i] = 1.0 / num_pages

def convergence_I(current, prev):
    max_diff = 0.0
    for i in range(len(current)):
        max_diff = max(max_diff, abs(current[i] - prev[i]))
    return max_diff

def main():
    global out_degrees
    edges = []
    num_vertices = 0

    while True:
        try:
            line = input()
            source, destination = map(int, line.split())
            num_vertices = max(num_vertices, max(source, destination) + 1)
            edges.append((source, destination))
        except EOFError:
            break

    node_degrees = [0] * num_vertices
    out_degrees = [0] * num_vertices

    h_matrix = defaultdict(list)
    for i in range(num_vertices):
        h_matrix[i] = []

    a_matrix = [0.0] * num_vertices

    G(h_matrix, a_matrix, edges, node_degrees)

    importance = [1.0 / num_pages if out_degrees[i] != 0 else 0.0 for i in range(len(h_matrix))]
    importance_prev = importance[:]

    I(h_matrix, a_matrix, importance)

    while convergence_I(importance, importance_prev) > 0.00001:
        importance_prev = importance[:]
        I(h_matrix, a_matrix, importance)

    sum = 0.0
    for i in range(len(importance)):
        if out_degrees[i] != 0:
            print(f"{i} = {importance[i]}")
            sum += importance[i]
    print(f"s = {sum}")

if __name__ == "__main__":
    main()
