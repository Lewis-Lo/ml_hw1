import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble, preprocessing, metrics

files = ['s20', 's19', 's18', 's17', 
        's16', 's15', 's14', 's13',
        's12', 's11', 's10', 's9',
        's8', 's7']

data = pickle.load(open(files[0], 'rb'))

for i in range(1, 14):
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

pickle.dump(knn, open('model_5.pickle', 'wb'))

# svc = svm.SVC(C=5)
# svc.fit(X_train, Y_train)
# print(svc.score(X_test, Y_test))

dtc = tree = DecisionTreeClassifier(criterion = 'entropy', max_depth=20, random_state=3)
dtc.fit(X_train, Y_train)
print(dtc.score(X_test, Y_test))
pickle.dump(dtc, open('dtc3.pickle', 'wb'))

forest = ensemble.RandomForestClassifier(n_estimators = 100)
forest_fit = forest.fit(X_train, Y_train)
print(forest.score(X_test, Y_test))
pickle.dump(forest, open('forest3.pickle', 'wb'))