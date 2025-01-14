from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# define a Gaussain NB classifier
clf1 = GaussianNB()
# define a SVM classifier
clf2 = SVC(kernel='poly', degree=3, max_iter=300000)
# define the class encodings and reverse encodings
clf = clf1
classes = {0: "Iris Setosa", 1: "Iris Versicolour", 2: "Iris Virginica"}
r_classes = {y: x for x, y in classes.items()}

# function to train and load the model during startup
def load_model():
    # load the dataset from the official sklearn datasets
    X, y = datasets.load_iris(return_X_y=True)
    # do the test-train split and train the model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    clf1.fit(X_train, y_train)
    # calculate and print the accuracy score for GaussianNB
    clf1_acc = accuracy_score(y_test, clf1.predict(X_test))
    print(f"Model GaussianNB trained with accuracy: {round(clf1_acc, 3)}")
    clf2.fit(X_train,y_train)
    # calculate and print the accuracy score for SVM
    clf2_acc = accuracy_score(y_test, clf2.predict(X_test))
    print(f"Model SVM trained with accuracy: {round(clf2_acc, 3)}")
    if clf1_acc >= clf2_acc:
        clf = clf1
        print("GaussianNB is best")
    else:
        clf = clf2
        print("SVM is best")  
    
# function to predict the flower using the model
def predict(query_data):
    x = list(query_data.dict().values())
    prediction = clf.predict([x])[0]
    print(f"Model prediction: {classes[prediction]}")
    return classes[prediction]

# function to retrain the model as part of the feedback loop
def retrain(data):
    # pull out the relevant X and y from the FeedbackIn object
    X = [list(d.dict().values())[:-1] for d in data]
    y = [r_classes[d.flower_class] for d in data]

    # fit the classifier again based on the new data obtained
    clf.fit(X, y)
