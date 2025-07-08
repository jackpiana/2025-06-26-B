import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMapNodes = {}


    def build_graph(self, year1, year2):
        self.grafo = None
        self.grafo = nx.Graph()
        self.idMapNodes = {}


        yearInf = year1
        yearSup = year2
        if yearInf > yearSup:
            yearInf = year2
            yearSup = year1

        idMapCircuits = DAO.getAllCircuits()


        for circuit in idMapCircuits.values():
            diz = dict()
            w = 0
            for year in range(yearInf+1, yearSup):
                results = DAO.getter_resCirYear(year, circuit.circuitId)
                diz[year] = results
                for r in results:
                    if r.time is not None:
                        w += 1
            self.idMapNodes[circuit.circuitId] = (circuit, w)
            self.grafo.add_node((circuit, w))

        edges = DAO.getter_edges(yearInf, yearSup)
        for e in edges:
            n1 = self.idMapNodes[e[0]]
            n2 = self.idMapNodes[e[1]]
            w = n1[1] + n2[1]
            self.grafo.add_edge(n1, n2, weight= w)

    def details(self):
        ccs = nx.connected_components(self.grafo)
        bestLen = 0
        bestcc = []
        for cc in ccs:
            if len(cc) > bestLen:
                bestLen = len(cc)
                bestcc = cc

        res = []

        for n in bestcc:
            pesoMin = 1000000000000000
            edges = list(self.grafo.edges(n, data=True))
            for e in edges:
                if e[2]['weight'] < pesoMin:
                    pesoMin = e[2]['weight']
            res.append((n, pesoMin))
        sorted_res = sorted(res, key=lambda x: x[1], reverse= True)
        return sorted_res

if __name__ == "__main__":
    m = Model()
    m.build_graph(2010, 2016)
    print(m.grafo)


