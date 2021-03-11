import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

files = ['data1_01.pickle', 'data1_02.pickle', 'data1_08.pickle']

data = pickle.load(open(files[0], 'rb'))

for i in range(1, 3):
    temp = pickle.load(open(files[i], 'rb'))
    data = np.hstack((data, temp))

data = data.T
dataX = data[:, 2:8]
dataY = data[:, 8]

X_train, X_test, Y_train, Y_test = train_test_split(dataX, dataY, test_size = 0.3)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, Y_train)

print(knn.predict(X_test))
print(Y_test)
print(knn.score(X_test, Y_test))

pickle.dump(knn, open('model1_04.pickle', 'wb'))