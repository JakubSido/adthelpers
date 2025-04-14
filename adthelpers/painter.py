import time
from collections.abc import Iterable
from queue import PriorityQueue

import matplotlib  # noqa: ICN001
import matplotlib.pyplot as plt
import networkx as nx

#import matplotlib.pyplot as plt, mpld3
print(matplotlib.matplotlib_fname())



def to_nx_graph(graph) -> nx.Graph:  # noqa: ANN001
    """Converts graph to networkx graph"""
    g = nx.Graph()
    if hasattr(graph, "nodes"):
        for content,node in graph.nodes.items():
            for weight,neighbor in node.neighbors:
                g.add_edge(content, neighbor.id, weight=weight)
    else:
        for source, neighbors in graph.edges.items():
            for weight, neighbor in neighbors:
                g.add_edge(source, neighbor, weight=weight)
    return g

class Painter:
    def on_press(self, event) -> None:  # noqa: ANN001
        if event.key == "n":
            self.paused = False

    def __init__(self, graph, visible: PriorityQueue | None = None,  # noqa: ANN001
                 closed: Iterable[int] | None = None,
                 color_edges: list[tuple[int, int]] | None = None,
                 wait_for_key: bool = False):  # noqa: FBT001, FBT002
        self.paused = wait_for_key
        self.wait_for_key = wait_for_key
        self.distances = None
        self.active = None
        self.visible = visible
        self.closed = closed
        self.graph = to_nx_graph(graph)
        self.color_edges = color_edges

        plt.ion()
        fig, self.ax = plt.subplots()
        fig.canvas.mpl_connect("key_press_event", self.on_press)
        plt.show(block=False)


    def _generate_color_map(self) -> list[str]:
        color_map = []
        for _, node, *_ in enumerate(self.graph):

            color = "grey"
            if self.visible is not None and self.visible.queue is not None \
                and node in [x[1] for _, x in self.visible.queue]:
                    color = "yellow"

            if self.closed is not None:
                try:
                    if node in self.closed:
                            color = "blue"
                except AttributeError:
                    pass

                if node in self.closed:
                    color = "blue"

            if self.active is not None and node == self.active:
                color = "red"

            color_map.append(color)
        return color_map

    def draw_graph(self, active = None) -> None:  # noqa: ANN001
        plt.cla()

        if isinstance(active, int):
            pass
        elif active is not None:
            self.active = active.id

        color_map = self._generate_color_map()

        pos = nx.spring_layout(self.graph, seed=2)


        nx.draw_networkx_nodes(
            self.graph,
            pos,
            ax=self.ax,
            node_color=color_map,
            node_size=1000,
        )

        node_labels = {}
        for n in self.graph.nodes:
            node_labels[n] = f"{n}"
            if self.distances is not None:
                node_labels[n] += "\n"+str(self.distances[n])



        # node_labels = {k: f"{k}{v}" for k, v in self.distances.items()}
        nx.draw_networkx_labels(self.graph, pos, ax=self.ax, labels=node_labels)

        e_colors = []
        if self.color_edges is not None:
            content_color_edges = [(fr, to) for fr,to in self.color_edges]

        for edge in self.graph.edges:
            e = (edge[0], edge[1])
            if self.color_edges is None:
                e_colors.append("grey")
            elif e in content_color_edges or (e[1], e[0]) in content_color_edges:
                e_colors.append("red")
            else:
                e_colors.append("grey")

        nx.draw_networkx_edges(
            self.graph,
            pos,
            ax=self.ax,
            edge_color=e_colors,
            edgelist=self.graph.edges(),
            node_size=1000,
        )

        edge_weights = nx.get_edge_attributes(self.graph, "weight")
        edge_labels = {edge: edge_weights[edge] for edge in self.graph.edges()}

        nx.draw_networkx_edge_labels(
            self.graph,
            pos,
            edge_labels=edge_labels,
            label_pos=0.3,
            font_size=7,
        )

        while self.paused and self.wait_for_key:
            time.sleep(0.01)
            plt.pause(0.01)
        self.paused=True
