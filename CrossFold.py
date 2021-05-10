from typing import List
import random
import math
import csv
class CrossFold:
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
            csv_file = csv.writer(f)
            # Get the length of each fold
            fold_length = math.floor(len(data)/fold_num)
            # number of left over data
            left_over = (len(data)-(fold_length*fold_num))
            # We add extra data inside
            fold_length += math.floor(left_over/fold_num)
            # Go through each fold and write to file
            for fold_counter in range(1, fold_num+1):
                csv_file.writerow(["fold"+str(fold_counter)])
                add_data = 0
                if left_over > 0:
                    add_data += 1
                for i in range(0, fold_length+add_data):
                    if len(data) > 0:
                        current_line = random.choice(data)
                        data.remove(current_line)
                        csv_file.writerow(current_line)
                    else:
                        break
                if (left_over > 0):
                    left_over -= 1
                if len(data) == 0:
                    break
            # Add left over data to the last fold
            while len(data) > 0:
                current_line = random.choice(data)
                csv_file.writerow(current_line)
                data.remove(current_line)
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
            print ("File cannot be opened {:s}".format(self.file_name))
            return None
        with f:
            # Strip all white space characters in line
            lines = [line.strip() for line in f]
            
            result = [CrossFold.convert_line_to_data(line) for line in lines]
            f.close()
        return result
    @staticmethod
    def convert_line_to_data(line:str):
        result = []
        try :
            result = []
            i = 2
            
            # collecting forbidden numbers
            temp = [v.strip().lower() for v in line.split(',')]
            for t in temp:
                try :
                    result.append(float(t))
                except ValueError:
                    # Meets non-number value
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
                        return [num_nearest, sample[-2:]]
                    except:
                        return None
                else:
                    return None
        return None
        