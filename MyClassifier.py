##ThreeDigits
import sys
from CrossFold import CrossFold
import numbers
import math
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
        # test if the values are within bound
        if self.training_data == None or column_no < 0 or column_no >= len(self.training_data):
            return None
        # Go through the training set and find the mean 
        # Since the input can be None or str, we only need to count values that actually exist
        n = 0
        sum_result = 0
        for line in self.training_data:
            current = line[column_no]
            if (isinstance(current, numbers.Number)):
                n += 1
                sum_result += current
        if n == 0:
            return 0
        return sum_result/n
    def find_standard_deviation(self, column_no:int):
        # test if the values are within bound
        if self.training_data == None or column_no < 0 or column_no >= len(self.training_data):
            return None
        mean = self.find_mean(column_no)
        sum_std = 0
        n = 0
        for line in self.training_data:
            current = line[column_no]
            if (isinstance(current, numbers.Number)):
                n += 1
                sum_std += pow((current-mean),2)
        if n <= 1:
            return 0
        return math.sqrt(sum_std/(n-1))
    def find_density(self, column_no:int, x:numbers.Number):
        # test if the values are within bound
        if self.training_data == None or column_no < 0 or column_no >= len(self.training_data):
            return None
        mean = self.find_mean(column_no)
        std_deviation = self.find_standard_deviation(column_no)
        factor = 1/(std_deviation*math.sqrt(2*math.pi))
        exp_hat = math.exp((-1*pow((x-mean), 2))/(2*pow(std_deviation,2)))
        return factor*exp_hat
    
    
#print(algorithm)
'''
GET ARGUMENTS
'''
if len(sys.argv) != 4:
    print("Wrong Input")
else :
    # Declare the class & then execute
    solution = MyClassifier(sys.argv[1].strip(), sys.argv[2].strip(), sys.argv[3].strip())
    print(solution.find_density(1, 0.16))
    