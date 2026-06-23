from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapShapes = {}
        self._bestPath = []
        self._bestScore = 0

    # BUILD GRAPH
    def buildGraph(self, anno, shape):
        self._graph.clear()
        self._buildNodes(anno, shape)
        self._idMapShapes = {s.id: s for s in self._graph.nodes()}
        self._buildEdges(anno, shape)

    def _buildNodes(self, anno, shape):
        avvistamenti = DAO.getAvvistamenti(anno, shape)
        self._graph.add_nodes_from(avvistamenti)

    def _buildEdges(self, anno, shape):
        edges = DAO.getEdges(anno, shape, self._idMapShapes)
        self._graph.add_edges_from(edges)

    # FIND PATH
    def buildPath(self):
        self._bestPath = []
        self._bestScore = 0

        mesiAvvistamenti = {i: [] for i in range(1,13)}

        for n in self._graph.nodes():
            parziale = [n]
            self._ricorsione(parziale, mesiAvvistamenti)

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, mesiAvvistamenti):
        ultimo_nodo = parziale[-1]
        # CONDIZIONE DI UPDATE
        if self._score(parziale) > self._bestScore:
            self._bestScore = self._score(parziale)
            self._bestPath = parziale.copy()

        # CONDIZIONE TERMINALE e BECKTRAKING
        for vicino in self._graph.neighbors(ultimo_nodo):
            if vicino.duration > ultimo_nodo.duration: # DURATA CRESCENTE
                mese_vicino = mesiAvvistamenti[vicino.datetime.month]
                if len(mese_vicino) < 3: # NON PIU DI 3 EVENTI PER MESE
                    mese_vicino.append(vicino)
                    parziale.append(vicino)
                    self._ricorsione(parziale, mesiAvvistamenti)
                    parziale.pop()
                    mesiAvvistamenti[vicino.datetime.month].pop()

    # AUX
    @staticmethod
    def _score(parziale):
        score = 0
        for i in range(0, len(parziale)):
            if i == 0:
                score += 100
            elif parziale[i].datetime.month == parziale[i-1].datetime.month:
                score += 200
            else:
                score += 100
        return score

    # METODI GETTER
    @staticmethod
    def getAllYears():
        DAO.getAllYears()

    @staticmethod
    def getAllShapes():
        DAO.getAllShape()

    def getInfoGraph(self):
        return len(self._graph.nodes()), len(self._graph.edges())

    def getNumWeaklyComponets(self):
        return len(list(nx.weakly_connected_components(self._graph)))

    def getBestComponente(self):
        # restituisce valore e sequenza della componente più lunga
        bestComponente = []
        for c in list(nx.weakly_connected_components(self._graph)):
            if len(c) > len(bestComponente):
                bestComponente = c
        return bestComponente, len(bestComponente)