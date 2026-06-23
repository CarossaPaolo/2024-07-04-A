from model.modello import Model

model = Model()

model.buildGraph(2005, "disk")
print(model.getInfoGraph())

print("==============")
print(f"componeti debolmente conesse: {model.getNumWeaklyComponets()}")

print("==============")
bComp, lBComp = model.getBestComponente()
print(f"best componte lunga {lBComp}")
for c in bComp:
    print(c)

print("==============")
bestPath, bestScore = model.buildPath()
print(f"punteggio: {bestScore}")
for i, n in enumerate(bestPath):
    print(f"{i}. ",n)
