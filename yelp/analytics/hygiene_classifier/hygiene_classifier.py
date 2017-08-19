import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import sklearn.metrics as metrics
from sklearn import svm
import numpy as np
import pandas as pd

cleaned_review_file = 'corpus/clean_reviews.txt'
training_label = 'Hygiene/training_hygiene.dat.labels'
additional = 'Hygiene/hygiene.dat.additional'

def read_data(file_name):
    with open (file_name, 'r') as f:
        text = f.readlines()
    return text

def save_file(output_file, data):
    with open ( output_file, 'w' ) as f:
        f.write('\n'.join(data))

def trained_feature_analysis(vectorizer, train_data_features):
    vocab = vectorizer.get_feature_names()
    print vocab

    # Sum up the counts of each vocabulary word
    dist = np.sum(train_data_features, axis=0)

    # For each, print the vocabulary word and the number of times it 
    # appears in the training set
    for tag, count in zip(vocab, dist):
        print count, tag             

def bow():
    corpus = read_data(cleaned_review_file)
    vectorizer = CountVectorizer(analyzer = "word", tokenizer = None,
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000, 
                             min_df = 2,
                             max_df = 0.5)

    train_data_features = vectorizer.fit_transform(corpus[:546])
    train_data_features = train_data_features.toarray()

    #trained_feature_analysis(vectorizer, train_data_features)

    return train_data_features

def main():
    train = pd.read_csv(training_label, header=0)
    
    data_features = bow()

    t_size = [50,100,150,200,250,300,350]
    #t_size = [330]

    names = ['Logistic Regression', 'SVM', 'Linear SVM', 'Decision Tree', 'Random Forest']
    classifiers = [LogisticRegression(), 
                    svm.SVC(),
                    svm.LinearSVC(), 
                    DecisionTreeClassifier(max_depth=5),
                    RandomForestClassifier(n_estimators = 100)]

    for i in t_size:
        train_data_features = data_features[:i, :]
        test_data_features = data_features[i:546, :]

        y_train = train['y'][:i]
        y_test = train['y'][i:546]

        for name, clf in zip(names, classifiers):

            #forest = RandomForestClassifier(n_estimators = 100)
            clf = clf.fit(train_data_features, y_train)
            y_pred = clf.predict(test_data_features)
            #prob = clf.predict_proba(test_data_features)

            f1_score = metrics.f1_score(y_test, y_pred)
            
            output = {}
            output['name'] = name
            output['train_size'] = i
            output['f1_score'] = f1_score
            
            print output

if __name__ == '__main__':
    main()