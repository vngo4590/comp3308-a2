#MyClassifier
import sys
class MyClassifier:
    def __init__(self, training_data_name:str, test_data_name:str,algo_type:str):
        '''
        Preprocess all data at the beginning so we can use them later on
        '''
        self.training_data = MyClassifier.read_file_data(training_data_name)
        self.test_data = MyClassifier.read_file_data(test_data_name)
        '''
            algo_type:
                None for invalid input
                array of length 1 for nb
                array of length 2 for number of nearest neighbor and type
        '''
        self.algo_type = MyClassifier.get_algo_type(algo_type)
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
            result = [MyClassifier.convert_line_to_data(line) for line in lines]
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
        

        
'''
GET ARGUMENTS
'''
if len(sys.argv) != 4:
    print("Wrong Input")
else :
    # Declare the class & then execute
    solution = MyClassifier(sys.argv[1].strip(), sys.argv[2].strip(), sys.argv[3].strip())