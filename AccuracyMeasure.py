from CrossFold import CrossFold
from MyClassifier import MyClassifier
'''
    In order to run this file, please comment out the functions running outside the class in MyClassifier.py
'''
def average(list_r):
    return sum(list_r) / len(list_r)
def find_accuracy_10_folds(src:str, type:str):
    result = []
    for i in range(1, 11):
        print(i)
        CrossFold.split_folder_to_files(src, i,"./tests/test.csv", "./tests/train.csv", "./tests/result.csv")
        solution = MyClassifier("./tests/train.csv", "./tests/test.csv", type)
        solution_result = solution.run()
        result_data = CrossFold.read_file_data("./tests/result.csv")
        total_data = len(result_data)
        count_correct = 0
        for r in range(0, total_data):
            if solution_result[r] == result_data[r][0]:
                count_correct += 1
        result.append(count_correct/total_data)
    return result
# Normal folds
CrossFold.fold_create("pima-folds.csv", CrossFold.read_file_data("pima.csv"))
# Run 10 folds in each
one_nn_results = find_accuracy_10_folds("pima-folds.csv", "1nn")
five_nn_results = find_accuracy_10_folds("pima-folds.csv", "5nn")
nb_results = find_accuracy_10_folds("pima-folds.csv", "nb")
print(one_nn_results)
print("Average 1NN (Normal): {:f}".format(average(one_nn_results)))
print(five_nn_results)
print("Average 5NN (Normal): {:f}".format(average(five_nn_results)))
print(nb_results)
print("Average Naive Bayes (Normal): {:f}".format(average(nb_results)))

# Normal folds
CrossFold.fold_create("pima-csf-folds.csv", CrossFold.read_file_data("pima-CFS.csv"))
# Run 10 folds in each
one_nn_results = find_accuracy_10_folds("pima-csf-folds.csv","1nn")
five_nn_results = find_accuracy_10_folds("pima-csf-folds.csv","5nn")
nb_results = find_accuracy_10_folds("pima-csf-folds.csv","nb")

print(one_nn_results)
print("Average 1NN (CFS): {:f}".format(average(one_nn_results)))
print(five_nn_results)
print("Average 5NN (CFS): {:f}".format(average(five_nn_results)))
print(nb_results)
print("Average Naive Bayes (CFS): {:f}".format(average(nb_results)))
