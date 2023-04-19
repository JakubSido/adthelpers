import time

import matplotlib
import networkx as nx
import matplotlib.pyplot as plt

#import matplotlib.pyplot as plt, mpld3
print(matplotlib.matplotlib_fname())




class Painter():
    def on_press(self,event):
        if event.key == 'n':
            self.wait_for_key = False

    def __init__(self, graph, visible, closed, active, distances=None, color_edges=None, wait_for_key=True):
        self.wait_for_key = wait_for_key
        self.distances = distances
        self.active = active
        self.visible = visible
        self.closed = closed
        self.graph = graph
        self.color_edges = color_edges

        plt.ion()
        fig, self.ax = plt.subplots()
        fig.canvas.mpl_connect('key_press_event', self.on_press)
        plt.show(block=False)



    def draw_graph(self, active=None):
        plt.cla()
        if active is not None:
            self.active = active
        color_map = []
        for i, node, *_ in enumerate(self.graph):
            if node in self.closed:
                color_map.append('blue')

            elif node == self.active:
                color_map.append('red')

            elif node in [x[1] for _, x in self.visible.queue]:
                color_map.append('yellow')

            else:
                color_map.append('grey')
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
        for e in self.graph.edges:
            if self.color_edges is None:
                e_colors.append("grey")
            elif e in self.color_edges:
                e_colors.append("red")
            elif (e[1], e[0]) in self.color_edges:
                e_colors.append("red")
            else:
                e_colors.append("grey")
        nx.draw_networkx_edges(self.graph, pos, ax=self.ax, edge_color=e_colors, edgelist=self.graph.edges(), node_size=1000)

        edge_weights = nx.get_edge_attributes(self.graph, 'weight')
        edge_labels = {edge: edge_weights[edge] for edge in self.graph.edges()}
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, label_pos=0.3, font_size=7)

        while self.wait_for_key:
            time.sleep(0.01)
            plt.pause(0.01)
        self.wait_for_key=True



