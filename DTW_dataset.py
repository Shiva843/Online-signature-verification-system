import csv
import os
from distance_calculation import calculate_distance

#distance calculation between each features

if __name__=='__main__':
    count1,count2=0,0
    output=1
    writer=csv.writer(open("new_dataset.csv",'w'))
    
    # Folder Path
    # path = "C:/Users/Nutan singh/Desktop/A2/dataset"
    path = r"C:\Users\Dell\Desktop\IITD\sem4\Biometric\AS-2\code\AS-2\dataset\set1"
    
    # Change the directory
    os.chdir(path)
    # iterate through all file
    for file1 in os.listdir():
        count1+=1
        for file2 in os.listdir():
            csv_input_list,csv_output_list=[],[]
            count2+=1
            # print (count1,count2)
            s1=file1[0:2]
            s2=file2[0:2]
            if s1==s2:
                output=1
            else:
                output=0
            file_path2 = f"{path}\{file2}"
            distance=calculate_distance(file1,file2)
            distance.append(output)
            # temp=read_text_file(file_path1,temp)
            # temp=read_text_file(file_path2,temp)
            # ls=[1,2,3,4,5,6,7]
            # csv_output_list.append(output)
            csv_input_list.append(distance)
            writer.writerows(csv_input_list)