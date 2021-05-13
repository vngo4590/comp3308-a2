from typing import List
import random
import math
import csv
class CrossFold:
    '''
    This method is used to look for fold inside the data
    '''
    @staticmethod
    def split_folder_to_files(fold_file_dir:str, fold_num:int, test_dir:str, train_dir:str, result_dir:str):
        fold_name = "fold"+str(fold_num)
        # Read the original data
        data = CrossFold.read_file_data(fold_file_dir)
        is_testing = False
        testing_set = []
        training_set = []
        result_set = []

        for line in data:
            if is_testing==False and len(line) == 1 and line[0].strip().lower() == fold_name:
                is_testing = True
            elif is_testing and len(line) == 1 and line[0].strip().lower() != fold_name:
                is_testing = False
            else:
                if (len(line) > 1):
                    if is_testing:
                        testing_set.append(line[:-1])
                        result_set.append(line[-1:])
                    else:
                        training_set.append(line)
        # Write data to files
        try:
            test_file = open(test_dir, 'w', newline='')
            train_file = open(train_dir, 'w', newline='')
            result_file = open(result_dir, 'w', newline='')
        except:
            raise("Unable to write to file")
            return None
        with test_file, train_file, result_file:
            csv_test = csv.writer(test_file)
            csv_train = csv.writer(train_file)
            csv_result = csv.writer(result_file)
            csv_test.writerows(testing_set)
            csv_train.writerows(training_set)
            csv_result.writerows(result_set)
    @staticmethod
    def class_to_insert(data:List, yes_leftover:int, no_leftover:int):
        yes_count = 0
        no_count = 0
        for line in data:
            if line[-1] == 'yes':
                yes_count += 1
            elif line[-1] == 'no':
                no_count += 1
        if no_count > yes_count:
            if yes_leftover > 0:
                return 'yes'
            elif no_leftover > 0:
                return 'no'
        elif no_count < yes_count:
            if no_leftover>0:
                return 'no'
            elif yes_leftover > 0:
                return 'yes'
        else:
            if yes_leftover > 0:
                return 'yes'
            elif no_leftover > 0:
                return 'no'
        return None
    @staticmethod
    def fold_create(fold_dir:str, data:List, fold_num:int=10):
        # Error checking
        if data == None or fold_num <= 0 or fold_num > len(data):
            return None
        try:
            f = open(fold_dir, 'w', newline='')
        except:
            raise("Unable to write to file")
            return None
        with f:

            # Yes List
            yes_list = list(filter(lambda line: line[-1].strip().lower()=='yes',data))
            # No List
            no_list = list(filter(lambda line: line[-1].strip().lower()=='no',data))
            # Left over list
            off_list = []
            offset = len(yes_list) - len(no_list)
            larger_list = None
            if offset < 0:
                larger_list = no_list
            elif offset > 0:
                larger_list = yes_list


            # How many do we need to extra values add per fold?
            num_input_offset = math.ceil(len(off_list)/fold_num)


            csv_file = csv.writer(f)
            # Get the length of each fold
            fold_length = math.floor((len(no_list)+len(yes_list) - abs(offset))/fold_num)

            fold_list = []
            current_class = 'yes'
            # Go through each fold and write to file
            for fold_counter in range(0, fold_num):
                fold_content = []
                for i in range(0, fold_length):
                    if current_class == 'yes' and len(yes_list) > 0:
                        current_line = random.choice(yes_list)
                        yes_list.remove(current_line)
                        fold_content.append(current_line)
                        current_class = 'no'
                    elif current_class == 'no' and len(no_list) > 0:
                        current_line = random.choice(no_list)
                        no_list.remove(current_line)
                        fold_content.append(current_line)
                        current_class = 'yes'
                fold_list.append(fold_content)
                if len(no_list) == 0 and len(yes_list) == 0:
                    break
            running = True
            while (len(yes_list)>0 or len(no_list)>0):

                for fold in fold_list:
                    class_insert = CrossFold.class_to_insert(fold, len(yes_list), len(no_list))
                    if class_insert == 'yes':
                        current_line = random.choice(yes_list)
                        yes_list.remove(current_line)
                        fold.append(current_line)
                    elif class_insert == 'no':
                        current_line = random.choice(no_list)
                        no_list.remove(current_line)
                        fold.append(current_line)
            # print(list(map(lambda fold: len(fold), fold_list)))
            # Put this value in odd dols
            fold_counter = 1
            for fold in fold_list:
                csv_file.writerow(["fold"+str(fold_counter)])
                csv_file.writerows(fold)
                csv_file.writerow([])
                fold_counter +=1
            f.close()
        return 0

    @staticmethod
    def read_file_data(data_dir:str):
        '''
        This function is dedicated to reading file input
        '''
        result = []
        try:
            f = open(data_dir, 'r')
        except OSError:
            print ("File cannot be opened {:s}".format(data_dir))
            return None
        with f:
            # Strip all white space characters in line
            result = [CrossFold.convert_line_to_data(line) for line in f]
            f.close()
        return result
    @staticmethod
    def convert_line_to_data(line:str):
        result = []
        try :
            result = []
            i = 2

            # collecting forbidden numbers
            temp = [v.strip() for v in line.split(',')]
            for t in temp:
                try :
                    result.append(float(t))
                except ValueError:

                    result.append(t)
                    continue
            i +=1
            return result
        except:
            print ("Wrong Input")
            return None
    @staticmethod
    def get_algo_type(algo_type:str):
        sample = algo_type.strip().lower()
        if (sample!=None):
            if (sample == 'nb'):
                return [sample]
            else:
                # test if the last 2 characters are nn
                if sample[-2:] == 'nn':
                    try:
                        num_nearest = int(sample[:-2])
                        return [sample[-2:],num_nearest]
                    except:
                        return None
                else:
                    return None
        return None
