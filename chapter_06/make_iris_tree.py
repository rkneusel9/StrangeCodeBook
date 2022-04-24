#
#  file:  make_iris_tree.py
#
#  A parsimonious decision tree for the iris dataset
#  from the SNOBOL chapter.  For the CLIPS example.
#
#  RTK, 08-May-2021
#  Last update:  08-May-2021
#
################################################################

import matplotlib.pylab as plt
import numpy as np
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.datasets import load_iris

iris = load_iris()

x_train = np.loadtxt("../SNOBOL/classifier/datasets/iris_train_data.txt")
y_train = np.loadtxt("../SNOBOL/classifier/datasets/iris_train_labels.txt")
x_test = np.loadtxt("../SNOBOL/classifier/datasets/iris_test_data.txt")
y_test = np.loadtxt("../SNOBOL/classifier/datasets/iris_test_labels.txt")

clf = DecisionTreeClassifier()
clf.fit(x_train, y_train)

fig = plt.figure(figsize=(25,20))
plot_tree(clf, feature_names=iris.feature_names, class_names=iris.target_names, filled=False)
fig.savefig("iris_tree.png")

print(clf.score(x_test, y_test))

