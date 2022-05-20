from pyvis.network import Network


class Graph:
    def __init__(self, nodes: []):
        self.nodes = nodes


class Node:
    def __init__(self, name: str, input_nodes: [], output_nodes: [], color: str):
        """
        constructor for Node object

        :param str name: represent the nodes name
        :param []  input_nodes: a list of all nodes entering this node
        :param [] output_nodes: a list of all nodes this node enters
        :param str color: represent the color of the machine
        :return Node object
        :rtype Node
        """
        self.name = name
        self.group_number = -1  # the group it belongs to
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        self.color = color


def visualise_graph(graph: Graph) -> None:
    """
    creats a visual model of the graph
    :param Graph graph:
    :return: None
    """
    net = Network(directed=True)
    nodes = []
    labels = []
    nodes_labels_dict = {}
    edges = []
    colors = []
    for n in range(len(graph.nodes)):
        node = graph.nodes[n]
        nodes.append(n)
        label = node.name
        labels.append(label + " group: " + str(node.group_number))
        nodes_labels_dict[graph.nodes[n]] = n
        colors.append(node.color)
    for n in graph.nodes:
        if n.output_nodes:
            for output_node in n.output_nodes:
                edges.append([nodes_labels_dict[n], nodes_labels_dict[output_node]])
    net.add_nodes(nodes, label=labels, color=colors)
    for edge in edges:
        net.add_edge(edge[0], edge[1])
    net.show('mygraph.html')


class GraphBuilder:
    def set_graph_num(self, cur_node: Node, next_graph_number: int) -> int:
        """
        sets the attribute num for a node given as a parameter

        :param Node cur_node: the node we want to set
        :param int next_graph_number: largest number of an existing group + 1
        :return: updated largest number of an existing group + 1
        :rtype int
        """
        if cur_node.group_number != -1:  # nodes num already have been set
            return next_graph_number
        changed = False  # indicates weather the num attribute have been updated
        if cur_node.input_nodes:  # has previous nodes
            cur_num = cur_node.input_nodes[0].group_number  # variable to check if any previous nodes have different numbers
            if [node for node in cur_node.input_nodes if node.group_number == -1]:
                return next_graph_number
            for node in cur_node.input_nodes:
                if node.group_number != cur_num or node.color != cur_node.color:  # the rule which separate between graphs
                    cur_node.group_number = next_graph_number
                    next_graph_number += 1
                    changed = True
                    break
        else:  # it is a root node
            cur_node.group_number = next_graph_number
            next_graph_number += 1
            changed = True
        if not changed:  # the node belongs to previous graph
            cur_node.group_number = cur_num
        if not cur_node.output_nodes:  # it is a leaf node
            return next_graph_number
        for output_node in cur_node.output_nodes:  # recursion
            next_graph_number = self.set_graph_num(output_node, next_graph_number)
        return next_graph_number

    def get_different_graphs(self, input_graph: Graph) -> []:
        """
        splits a graph into different smaller graphs according to dependencies and machines
        ./
        :param Graph input_graph: a list of nodes
        :return: a list of graphs
        """
        graphs = []  # list of different graphs by order
        nodes = []  # will use to make each graph
        cur_graph_num = 1
        for input_node in input_graph.nodes:
            if not input_node.input_nodes:  # I want to start the recursion in a root node
                cur_graph_num = self.set_graph_num(input_node, cur_graph_num)
        for graph_num in range(1, cur_graph_num):
            for node in input_graph.nodes:
                if node.group_number == graph_num:
                    nodes.append(node)
            graphs.append(Graph(nodes))
            nodes = []
        return graphs


def example_one():
    A = Node("A", [], [], "blue")
    C = Node("C", [A], [], "orange")
    B = Node("B", [A], [], "blue")
    D = Node("D", [], [C], "orange")
    E = Node("E", [C, D], [], "orange")
    F = Node("F", [B], [], "green")
    G = Node("G", [C, B], [], "green")
    A.output_nodes.extend([C, B])
    C.input_nodes.append(D)
    C.output_nodes.extend([E, G])
    B.output_nodes.extend([G, F])
    D.output_nodes.append(E)
    original_graph = Graph([A, B, C, D, E, F, G])
    graph_builder = GraphBuilder()
    output_list_of_graphs = graph_builder.get_different_graphs(original_graph)
    visualise_graph(graph=original_graph)


def example_from_interview():
    A = Node("A", [], [], "blue")
    B = Node("B", [A], [], "blue")
    C = Node("C", [B], [], "blue")
    X = Node("X", [B], [], "orange")
    E = Node("E", [C, X], [], "blue")
    F = Node("F", [E], [], "blue")
    A.output_nodes.append(B)
    B.output_nodes.extend([X, C])
    C.output_nodes.append(E)
    X.output_nodes.append(E)
    E.output_nodes.append(F)
    original_graph = Graph([A, B, C, X, E, F])
    graph_builder = GraphBuilder()
    output_list_of_graphs = graph_builder.get_different_graphs(original_graph)
    visualise_graph(graph=original_graph)


if __name__ == '__main__':
    example_one()
    # example_from_interview()



