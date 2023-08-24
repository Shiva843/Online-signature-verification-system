import math
from  reference import reference_features_list

def DTW(Q_list,R_list):
    #cost matrix
    cost = [[0 for x in range(len(R_list))] for y in range(len(Q_list))] 
    for i in range(0,len(Q_list)):
        for j in range(0,len(R_list)):
            cost[i][j]=abs(Q_list[i]-R_list[j])
    #dtw algorithm
    dtw_arr = [[0 for x in range(len(R_list)+1)] for y in range(len(Q_list)+1)] 
    for i in range(0,len(Q_list)+1):
        dtw_arr[i][0]=math.inf
    for j in range(0,len(R_list)+1):
        dtw_arr[0][j]=math.inf
    dtw_arr[0][0]=0
    for i in range(1,len(Q_list)+1):
        for j in range(1,len(R_list)+1):
            dtw_arr[i][j] = cost[i-1][j-1] + min(min(dtw_arr[i-1][j],dtw_arr[i][j-1]),dtw_arr[i-1][j-1])
    return dtw_arr[len(Q_list)][len(R_list)]

def calculate_distance(reference_file,test_file):
    
    reference_list=reference_features_list(reference_file)
    # query signature       
    test_list=reference_features_list(test_file)

    distance=[]
    for i in range(0,12):
        distance.append(DTW(reference_list[i],test_list[i]))    
    return distance
