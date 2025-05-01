import networkx as nx
import random
import logging
import argparse
import pandas as pd

logging.basicConfig(level=logging.INFO,filename=f"./graph_generator.log")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def test_im_gen_manual_hard(manual= True, bit=2, num_nodes=30, a=1.2, c=0.3, th_min=0.25):
    # probability of adding a edge
    max_num_in_edges = 2**bit

    graph = nx.DiGraph()
    for i in range(num_nodes):
        graph.add_node(i)

    edge_count = 0

    # manually add edges
    if manual:
        # for i in range(num_nodes,0,-1):
        for i in range(num_nodes):
            p = c * ((1- i / num_nodes) ** (a - 1))
            # print(f"p-{p} - {i}")
            num_edges_added = 0
            for j in range(i+1,num_nodes):
                status = 1 if random.random() < p else 0

                if status:
                    # if graph.in_degree(j)<max_num_in_edges:
                    num_edges_added += 1
                    graph.add_edge(i,j)
                    edge_count+=1
                    logger.info(f"Ddd edge {i,j}")

            # print(f"num edges added {num_edges_added}")
    else:
        graph  = generate_dag(num_nodes)

    is_acyclic = nx.is_directed_acyclic_graph(graph)
    # print(f"is_acyclic {is_acyclic}")
    graph=limit_indegree_to_N(graph)

    # for node in graph.nodes:
    #     print(f"{node} - {graph.in_degree(node)} - {graph.out_degree(node)}")

    th_samples = []
    for i in range(1, 2**bit):
        th = i/(2**bit)
        if th >= th_min:
            th_samples.append(i/(2**bit))
    for node in graph.nodes():
        graph.nodes[node]['thresh'] = random.choice(th_samples)
        in_edges = graph.in_edges(node)
        if len(list(in_edges)) == 4:
            for edge in in_edges:
                graph.edges[edge]['weight'] = 0.25
        elif len(list(in_edges)) == 1:
            for edge in in_edges:
                graph.edges[edge]['weight'] = random.choice([0.25,0.5,0.75])
        elif len(list(in_edges)) == 2:
            for edge in in_edges:
                graph.edges[edge]['weight'] = random.choice([0.25,0.5])
        elif len(list(in_edges)) == 3:
            for edge in in_edges:
                graph.edges[edge]['weight'] = 0.25

    return graph



def test_im_gen_manual(manual= True, bit=2, num_nodes=30, p_high =0.7, p_low=0.4, th_min=0.25):
    max_num_in_edges = 2**bit

    graph = nx.DiGraph()
    for i in range(num_nodes):
        graph.add_node(i)

    edge_count = 0

    # manually add edges
    if manual:
        for i in range(num_nodes):
            for j in range(i+1,num_nodes):
                if i <num_nodes/10:
                    status = 1 if random.random() < p_high else 0
                else:
                    status = 1 if random.random() < p_low else 0

                if status:
                    if graph.in_degree(j)<max_num_in_edges:
                        graph.add_edge(i,j)
                        edge_count+=1
                        logger.info(f"Ddd edge {i,j}")
    else:
        graph  = generate_dag(num_nodes)

    is_acyclic = nx.is_directed_acyclic_graph(graph)
    # print(f"is_acyclic {is_acyclic}")
    # print(f"number of edges: {graph.number_of_edges()}")
    # for i in range(num_nodes):
    #     print(f"node {i} has {graph.in_degree(i)} in edges and {graph.out_degree(i)} out edges")

    th_samples = []
    for i in range(1, 2**bit):
        th = i/(2**bit)
        if th >= th_min:
            th_samples.append(i/(2**bit))
    for node in graph.nodes():
        graph.nodes[node]['thresh'] = random.choice(th_samples)
        in_edges = graph.in_edges(node)
        if len(list(in_edges)) == 4:
            for edge in in_edges:
                graph.edges[edge]['weight'] = 0.25
        elif len(list(in_edges)) == 1:
            for edge in in_edges:
                graph.edges[edge]['weight'] = random.choice([0.25,0.5,0.75])
        elif len(list(in_edges)) == 2:
            for edge in in_edges:
                graph.edges[edge]['weight'] = random.choice([0.25,0.5])
        elif len(list(in_edges)) == 3:
            for edge in in_edges:
                graph.edges[edge]['weight'] = 0.25

    return graph


def limit_indegree_to_N(DAG, N=4):
    """
    Modifies the DAG so that no node has in-degree greater than N
    by removing edges randomly.

    Parameters:
    - DAG: A directed acyclic graph (e.g., networkx.DiGraph)
    - N: Maximum allowed in-degree for any node
    """
    for node in list(DAG.nodes):
        in_edges = list(DAG.in_edges(node))
        if len(in_edges) > N:
            edges_to_remove = random.sample(in_edges, len(in_edges) - N)
            DAG.remove_edges_from(edges_to_remove)

    return DAG

def can_add_edge(dag, source, target):
    # Check if adding an edge creates a cycle (making sure the graph remains a DAG)
    if has_path(dag, target, source):
        return False
    # Check if the in-degree of the target will exceed 4
    if dag.in_degree(target) >= 4:
        return False
    return True

def has_path(dag, source, target):
    # NetworkX utility to check if a path exists (used to detect potential cycles)
    return nx.has_path(dag, source, target)

def generate_dag(nodes_count, info=False):
    # Initialize a directed graph
    dag = nx.DiGraph()
    # Add nodes
    dag.add_nodes_from(range(nodes_count))
    # Attempt to add edges without violating DAG nature and in-degree condition
    for _ in range(nodes_count * 4):  # Arbitrary number of attempts
        source, target = random.sample(dag.nodes(), 2)
        if can_add_edge(dag, source, target):
            dag.add_edge(source, target)
            # Check if we should stop (optional, depends on when you consider the graph "complete")
            if all(dag.in_degree(n) >= 4 for n in dag.nodes()):
                break
    if info:
        print(f"nodes: {dag.number_of_nodes()}")
        print(f"edges: {dag.number_of_edges()}")
        print(f"in degree : {dag.in_degree()}")
        print(f"out degree : {dag.out_degree()}")
        print(f"DAG: {nx.is_directed_acyclic_graph(dag)}")
    return dag

def write_graph_to_file(random_weighted_directed_graph, path_to_graph):
    with open(path_to_graph, 'w') as f:
        for node in random_weighted_directed_graph.nodes(data=True):
            node_id, node_data = node
            # print(node_data)
            f.write(f"{node_id} {node_data['thresh']}\n")
        for edge in random_weighted_directed_graph.edges(data=True):
            source, target, edge_data = edge
            # print(edge_data)
            f.write(f"{source} {target} {edge_data['weight']}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="IM graph generation script.")
    parser.add_argument("--path_to_dir", type=str, default='./', help="Path to generated file")
    parser.add_argument("--num_graph", type=int, default=100, help="Number of graphs to generate")
    parser.add_argument("--num_nodes", type=int, default=100, help="Number of nodes per graph")
    parser.add_argument("--th_min", type=float, default=0.5, help="Minimum threshold for filtering")
    parser.add_argument("--higher_deth", type=float, default=0.5, help="Minimum threshold for filtering")
    parser.add_argument("--hard", action='store_true', help="Generate hard IM problems with higher depth")
    parser.add_argument("--a", action='float', default=1.5,help="Coefficient of 'a' in hard IM problem generation.")
    parser.add_argument("--c", action='float', default=0.4,help="Coefficient of 'c' in hard IM problem generation.")
    parser.add_argument("--p_high", action='float', default=0.2,help="Probability upper bound in easy IM problem generation")
    parser.add_argument("--p_low", action='float', default=0.1,help="Probability lower bound in easy IM problem generation")

    args = parser.parse_args()

    num_graph = args.num_graph
    num_nodes = args.num_nodes
    th_min = args.th_min
    path_to_dir = args.path_to_dir
    a=args.a
    c=args.c
    p_high = args.p_high
    p_low = args.p_low

    data = {
        'graph': [],
        'nodes': [],
        'edges': [],
        'max_in_degree': [],
        'min_in_degree': [],
        'max_out_degree': [],
        'min_out_degree': []
    }
    for n in range(num_graph):
        if args.hard:
            graph = test_im_gen_manual_hard(manual=True, bit=2, num_nodes=num_nodes, a=a, c=c, th_min=th_min)
        else:
            graph = test_im_gen_manual(manual=True, bit=2, num_nodes=num_nodes, p_high=p_high, p_low=p_high, th_min=th_min)

        # Get the maximum out-degree
        out_degree = dict(graph.out_degree()).values()
        max_out_degree = max(out_degree)
        min_out_degree = min(out_degree)
        # Get the maximum in-degree
        in_degree = dict(graph.in_degree()).values()
        min_in_degree = min(in_degree)
        max_in_degree = max(in_degree)
        data['graph'].append(n)
        data['nodes'].append(num_nodes)
        data['edges'].append(graph.number_of_edges())
        data['max_in_degree'].append(max_in_degree)
        data['min_in_degree'].append(min_in_degree)
        data['max_out_degree'].append(max_out_degree)
        data['min_out_degree'].append(min_out_degree)
        path_to_graph = f"{path_to_dir}/graph_{n}.g"

        # print(path_to_graph)
        write_graph_to_file(graph, path_to_graph)

    #df = pd.DataFrame(data)
    #print(df)
    # df.to_csv(f"{path_to_dir}/summary.csv")