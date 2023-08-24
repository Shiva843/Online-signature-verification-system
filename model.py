import csv
import sys
from distance_calculation import calculate_distance
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



def adaboost_model():
    
    input_list,output_list=[],[]
    with open('new_dataset.csv', mode ='r')as file:
    
    # reading the CSV file
        csvFile = csv.reader(file)
        
        # displaying the contents of the CSV file
        for lines in (csvFile):
                # print(lines)
            if len(lines)!=0:
                ls=[]
                for i in range(0,len(lines)-1):
                    ls.append(float(lines[i]))
                input_list.append(ls)
                output_list.append(float(lines[-1]))
    

    #training

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(input_list, output_list, test_size=0.3)
    # print(X_train,X_test,y_train,y_test)

    # Create adaboost classifer object
    abc = AdaBoostClassifier(n_estimators=50, learning_rate=0.5, random_state=0)

    # Train Adaboost Classifer
    model = abc.fit(X_train, y_train)
    importance = model.feature_importances_
    # print(importance)
    y_pred = model.predict(X_test)
    # calculate and print model accuracy
    score=accuracy_score(y_test, y_pred)
    # print("AdaBoost Classifier Model Accuracy:", score)
    return importance, model

if __name__=='__main__':

    file_name=sys.argv[0]
    reference_file=sys.argv[1]
    test_file=sys.argv[2]

    distance=calculate_distance(reference_file,test_file)
    importance,model=adaboost_model()
    
    similarity_score=0
    for i in range(0,12):
        similarity_score+=importance[i]*distance[i]
    # if (model.predict([distance])):
    #     print ("signature is matched")
    # else:
    #     print ("signature is not matched")
    print("Weighted_similarity_score",similarity_score)
