import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMapNodes = {}
        self.componenteMigliore = []
        self.k = 1

        self.bestPath = []
        self.bestScore = 0


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
            np = 0
            npt = 0
            for year in range(yearInf+1, yearSup):
                results = DAO.getter_resCirYear(year, circuit.circuitId)
                diz[year] = results
                for r in results:
                    npt += 1
                    if r.time is not None:
                        np += 1
            self.idMapNodes[circuit.circuitId] = (circuit, np, npt)
            self.grafo.add_node((circuit, np, npt))

        edges = DAO.getter_edges(yearInf, yearSup)
        for e in edges:
            n1 = self.idMapNodes[e[0]]
            n2 = self.idMapNodes[e[1]]
            w = n1[1] + n2[1]
            self.grafo.add_edge(n1, n2, weight= w)

    def details(self):
        ccs = nx.connected_components(self.grafo)
        bestLen = 0
        for cc in ccs:
            if len(cc) > bestLen:
                bestLen = len(cc)
                self.componenteMigliore = list(cc)

        res = []

        for n in self.componenteMigliore:
            pesoMin = 1000000000000000
            edges = list(self.grafo.edges(n, data=True))
            for e in edges:
                if e[2]['weight'] < pesoMin:
                    pesoMin = e[2]['weight']
            res.append((n, pesoMin))
        sorted_res = sorted(res, key=lambda x: x[1], reverse= True)
        return sorted_res


    def calcola_bestpath(self, k, m, year1, year2): #k: numero di gare max della path --- m: numero minimo di gp corsi nel circuit perchè sia considerato
        self.details()

        self.k = k
        yearInf = year1
        yearSup = year2
        if yearInf > yearSup:
            yearInf = year2
            yearSup = year1

        insieme_iniziale = []
        for n in self.componenteMigliore:
            gareInRange = DAO.getter_numeroGare_inRange(n[0].circuitId, yearInf, yearSup)
            print(gareInRange)
            if gareInRange >= m:
                insieme_iniziale.append(n)
        print(insieme_iniziale)

        self.ricorsione([], insieme_iniziale)

    def ricorsione(self, parziale, insieme_iniziale):
        if self.isAmmissibile(parziale):
            self.calcolaPunteggio(parziale)
        elif (insieme_iniziale) != None:
            for n in insieme_iniziale:
                parz = parziale.copy()
                parziale.append(n)
                insieme_iniziale = insieme_iniziale.copy()
                insieme_iniziale.remove(n)
                print(insieme_iniziale)
                self.ricorsione(parz, insieme_iniziale)
                parziale.pop()

    def isAmmissibile(self, parziale):
        if len(parziale) == self.k:
            return True

    def calcolaPunteggio(self, parziale):
        score = 0
        for n in parziale:
            scoreGara = (1 - (n[1] / n[2]))
            score += scoreGara
        print(score)
        if score > self.bestScore:
            self.bestScore = score
            self.bestPath = parziale


if __name__ == "__main__":
    m = Model()
    m.build_graph(2010, 2016)
    print(m.grafo)
    m.calcola_bestpath(4, 2, 2000, 2004)
    print(m.bestScore, m.bestPath)


