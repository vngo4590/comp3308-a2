##ThreeDigits
import sys
from CrossFold import CrossFold
import numbers
class MyClassifier:
    def __init__(self, training_data_name:str, test_data_name:str,algo_type:str):
        '''
        Preprocess all data at the beginning so we can use them later on
        '''
        self.training_data = CrossFold.read_file_data(training_data_name)
        self.test_data = CrossFold.read_file_data(test_data_name)
        '''
            algo_type:
                None for invalid input
                array of length 1 for nb
                array of length 2 for number of nearest neighbor and type
        '''
        self.algo_type = CrossFold.get_algo_type(algo_type)
        self.accuracy = 0
    def find_mean(self, column_no:int):
        # Go through the training set and find the mean 
        # Since the input can be None or str, we only need to count values that actually exist
        n = 0
        sum = 0
        return 0
            

        
# from nodes import Node
# from tree import Tree

#print(algorithm)
'''
GET ARGUMENTS
'''
if len(sys.argv) != 4:
    print("Wrong Input")
else :
    # Declare the class & then execute
    solution = MyClassifier(sys.argv[1].strip(), sys.argv[2].strip(), sys.argv[3].strip())
    CrossFold.split_folder_to_files("pima-folds.csv", 1, "test.csv", "train.csv", "result.csv")