import time

import matplotlib
import networkx as nx
import matplotlib.pyplot as plt

#import matplotlib.pyplot as plt, mpld3
print(matplotlib.matplotlib_fname())

def to_nx_graph(graph):
    '''Converts graph to networkx graph'''
    G = nx.Graph()
    for content,node in graph.nodes.items():
        for weight,neighbor in node.neighbors:
            G.add_edge(content, neighbor.id, weight=weight)
    return G

class Painter():
    def on_press(self,event):
        if event.key == 'n':
            self.paused = False

    def __init__(self, graph, visible=None, closed=None, active=None, distances=None, color_edges=None, wait_for_key=False):
        self.paused = wait_for_key
        self.wait_for_key = wait_for_key
        self.distances = distances
        self.active = active
        self.visible = visible
        self.closed = closed
        self.graph = to_nx_graph(graph)
        self.color_edges = color_edges

        plt.ion()
        fig, self.ax = plt.subplots()
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        plt.show(block=False)



    def draw_graph(self, active=None):
        plt.cla()
        
        if active is not None:
            self.active = active.id
        
        color_map = []
        for i, node, *_ in enumerate(self.graph):
            
            color = 'grey'
            if self.visible is not None and self.visible.queue is not None:
                if node in [x[1] for _, x in self.visible.queue]:
                    color = 'yellow'    

            if self.closed is not None:
                if node in [x.id for x in self.closed]:
                    color = 'blue'

            if self.active is not None and node == self.active:
                color = 'red'    


            
            color_map.append(color)
        pos = nx.spring_layout(self.graph, seed=2)


        nx.draw_networkx_nodes(self.graph, pos, ax=self.ax, node_color=color_map, node_size=1000)

        node_labels = dict()
        for n in self.graph.nodes:
            node_labels[n] = f'{n}'
            if self.distances is not None:
                node_labels[n] += "\n"+str(self.distances[n])



        # node_labels = {k: f"{k}{v}" for k, v in self.distances.items()}
        nx.draw_networkx_labels(self.graph, pos, ax=self.ax, labels=node_labels, )

        e_colors = []
        if self.color_edges is not None:
            content_color_edges = [(fr, to) for fr,to in self.color_edges]
        
        for e in self.graph.edges:
            e = (e[0], e[1])
            if self.color_edges is None:
                e_colors.append("grey")
            elif e in content_color_edges:
                e_colors.append("red")
            elif (e[1], e[0]) in content_color_edges:
                e_colors.append("red")
            else:
                e_colors.append("grey")
        nx.draw_networkx_edges(self.graph, pos, ax=self.ax, edge_color=e_colors, edgelist=self.graph.edges(), node_size=1000)

        edge_weights = nx.get_edge_attributes(self.graph, 'weight')
        edge_labels = {edge: edge_weights[edge] for edge in self.graph.edges()}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)

        while self.paused and self.wait_for_key:
            time.sleep(0.01)
            plt.pause(0.01)
        self.paused=True



