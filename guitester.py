import random, time
from matrixGui import NeoMatrixGui
gui = NeoMatrixGui(15,30)
matrix = [[(random.randint(0,255), random.randint(0,255), random.randint(0,255)) for j in range(30)] for i in range(15)]
gui.set_matrix(matrix)
print("before")

time.sleep(1)
for x in range(5):
    matrix[random.randint(0,14)][random.randint(0,29)] = (0,0,0)
gui.set_matrix(matrix)
gui.submit_all()
