#MyClassifier
import sys
from CrossFold import CrossFold
import numbers
import math
from typing import List
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
        # Result storing yes or no
        self.result = []
    def find_euclidean(self, train:List, test:List):
        if (train == None or test == None):
            return None
        train_sample = train[:-1]
        if (len(train_sample) != len(test)):
            return None
        sum_eu = 0
        for i in range(0, len(train_sample)):
            if isinstance((train_sample[i]), numbers.Number) and isinstance((test[i]), numbers.Number):
                sum_eu += (train_sample[i]-test[i]) ** 2
        return math.sqrt(sum_eu)

    def find_mean(self, column_no:int, class_str:str):
        class_type = class_str

        # Go through the training set and find the mean
        # Since the input can be None or str, we only need to count values that actually exist
        n = 0
        sum_result = 0
        for line in self.training_data:
            if column_no < len(line):
                current = line[column_no]
                if (isinstance(current, numbers.Number) and line[-1] == class_type):
                    n += 1
                    sum_result += current
        if n == 0:
            return 0
        return sum_result/n
    def find_standard_deviation(self, column_no:int, class_str:str):
        class_type = class_str
        mean = self.find_mean(column_no, class_type)
        sum_std = 0
        n = 0
        for line in self.training_data:
            if column_no < len(line):
                current = line[column_no]
                if (isinstance(current, numbers.Number) and line[-1] == class_type):
                    n += 1
                    sum_std += (current - mean) ** 2
        if n <= 1:
            return None
        return (sum_std/(n-1))**(1/2)
    # column 0 to len(n)-1
    def find_density(self, column_no:int, x:numbers.Number, class_str: str):
        class_type = class_str
        if (class_type == None):
            return None
        # test if the values are within bound
        if self.training_data == None or column_no < 0 or column_no >= len(self.training_data):
            return None
        mean = self.find_mean(column_no, class_type)
        std_deviation = self.find_standard_deviation(column_no, class_type)
        if (std_deviation==None or std_deviation==0 or mean==None):
            return None
        factor = 1/(std_deviation*((2*math.pi)**(1/2)))
        exp_hat = math.exp((-1)*(((x - mean) ** 2))/(2*(std_deviation ** 2)))
        return factor*exp_hat
    def k_nearest_neighbors(self, test:List, neighbors_no:int):
        '''
        From the training set, begin to search for k nearest neighbors
        return either yes or no
        :param test: one line from the test set
        :param neighbors_no: number of neighbours
        :return: yes or no
        '''
        distances = []
        for train_data in self.training_data:
            dist = self.find_euclidean(test, train_data)
            distances.append(dist)
        ordered_dist = sorted(distances)
        neighbours = []
        for nums in ordered_dist:
            i = 0
        while i < neighbors_no:
            close_no = ordered_dist(i)
            neighbours.append(close_no)
            i = i + 1
        classes = []
        for line in neighbours:
            cols = line.split(',')
            classes.append(cols[len(cols) - 1])
        yes = 0
        no = 0
        for ans in classes:
            if ans == 'yes':
                yes = yes + 1
            elif ans = 'no':
                no = no + 1
        if yes > no:
            return "yes"
        else:
            return "no"
    def count_class(self, class_str:str):
        class_type = class_str
        count = 0
        for line in self.training_data:
            if (line[-1] == class_type):
                count += 1
        return count

    def naive_bayes(self, test:List):
        '''
        From the training set, begin to search for value using Naive Bayes
        return either yes or no
        :param test: one line from the test set
        :return: yes or no
        '''
        # Count yes and no's
        yes_count = self.count_class('yes')
        no_count = self.count_class('no')
        total_class_count = yes_count + no_count
        yes_result = yes_count/total_class_count
        no_result = no_count/total_class_count
        for i in range(0, len(test)):
            yes_result *= self.find_density(i, test[i], 'yes')
            no_result *= self.find_density(i, test[i], 'no')
        if no_result > yes_result:
            return "no"
        else:
            return "yes"
    def run(self):
        '''
        main function to execute the algorithms. This function will call k_nearest neighbors or naive_bayes directly.
        Print output
        :return: array of results
        '''
        if (self.algo_type == None):
            print("Incorrect function type")
            return None
        elif len(self.algo_type)==2 and (self.algo_type[1] < 1 or self.algo_type[1] > len(self.training_data)):
            print("Incorrect number of neighbours")
            return None
        '''
        Run program and then execute the algo
        '''
        algo_type_str = self.algo_type[0]
        if algo_type_str == 'nn':
            self.result = [self.k_nearest_neighbors(test, self.algo_type[1]) for test in self.test_data]
        elif algo_type_str == 'nb':
            self.result = [self.naive_bayes(test) for test in self.test_data]
        return self.result


#print(algorithm)
'''
GET ARGUMENTS
'''
if len(sys.argv) != 4:
    print("Wrong Input")
else :
    # Declare the class & then execute
    solution = MyClassifier(sys.argv[1], sys.argv[2], sys.argv[3])
    # Print result
    [print(n) for n in solution.run()]
    # CrossFold.fold_create("pima-folds.csv", CrossFold.read_file_data("pima.csv"))
    # CrossFold.split_folder_to_files("pima-folds.csv", 1,"./tests/simple_naive_test.csv", "./tests/simple_naive_train.csv", "./tests/simple_naive.out")

    '''
    Example of using euclidean
    print(solution.find_euclidean([1, 0.1, 3.9, "yes"], [1, 2, 0.3]))
    '''
