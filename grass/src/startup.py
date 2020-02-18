from main import add


for i in range(2):
    for j in range(2):
        add.delay(i, j)
