# Import necessary modules
import random

def main():
    pass

def split_training_testing(data, p_test = 20):
    """Splits the data into training and testing sets based on the given ratio.
    Args:
        data (list): The dataset to be split.
        p_test (int|float): The proportion of the data to be used for testing from 0 to 100."""
    
    # Validate inputs
    assert type(data) == list, "Data must be a list."
    assert type(p_test) == int or type(p_test) == float, "Test ratio must be an integer or float."
    assert 0 < p_test < 100, "Test ratio must be between 0 and 100."
    assert len(data) > 1, "Data must have more than one value."
    
    # Get the test size
    n = len(data)
    test_size = round(n * p_test/100)

    # Split the data for the test set
    test_indexes = random.sample(range(n), k = test_size)
    test_set = [data[i] for i in test_indexes]

    # Split the data for the train set
    train_set = [data[i] for i in range(n) if i not in test_indexes]

    return train_set, test_set

def confusion_matrix(predicted, actual, positive = 1):
    """Generates the values of a confusion matrix from actual and predicted labels.
    It returns the values in the order: TP, FP, TN, FN.
    Args:
        predicted(list): The predicted values from the model.
        actual (list): The list of actual/true values.
        positive (int|float|str): The class considered as positive."""
    
    # Validate inputs
    assert type(predicted) == list, "Predicted values must be a list."
    assert type(actual) == list, "Actual/true values must be a list."
    assert len(predicted) == len(actual), "Predicted and actual values must have the same length."
    assert len(predicted) > 0, "Predicted and actual values must have at least one element."
    assert type(positive) == int or type(positive) == float or type(positive) == str

    # Initialize the confusion matrix
    matrix = {'TP': 0, 'FP': 0, 'FN': 0, 'TN': 0}
    
    # Populate the confusion matrix
    for i in range(len(predicted)):
        if predicted[i] == actual[i] and predicted[i] == positive:
            matrix['TP'] += 1
        elif predicted[i] == actual[i] and predicted[i] != positive:
            matrix['TN'] += 1
        elif predicted[i] != actual[i] and predicted[i] == positive:
            matrix['FP'] += 1
        elif predicted[i] != actual[i] and predicted[i] != positive:
            matrix['FN'] += 1
    
    # Return the confusion matrix values
    return matrix['TP'], matrix['FP'], matrix['TN'], matrix['FN']

def accuracy(TP, FP, TN, FN):
    """Calculates accuracy from confusion matrix values.
    Proportion of correct predictions (both true positives and true negatives).
    Args:
        TP (int): True Positives.
        FP (int): False Positives.
        TN (int): True Negatives.
        FN (int): False Negatives."""
    
    # Validate inputs
    assert all(type(i) == int for i in [TP, FP, TN, FN]), "All inputs must be integers."
    assert all(i >= 0 for i in [TP, FP, TN, FN]), "All inputs must be equal or greater than 0."

    # Calculate and return accuracy
    try:
        return (TP + TN) / (TP + TN + FP + FN)
    except ZeroDivisionError:
        return float('nan')

def sensitivity(TP, FN):
    """Calculates sensitivity (recall) from confusion matrix values.
    Proportion of actual positives correctly identified.
    Args:
        TP (int): True Positives.
        FN (int): False Negatives."""
    
    # Validate inputs
    assert all(type(i) == int for i in [TP, FN]), "All inputs must be integers."
    assert all(i >= 0 for i in [TP, FN]), "All inputs must be equal or greater than 0."
    
    # Calculate and return sensitivity
    try:
        return TP / (TP + FN)
    except ZeroDivisionError:
        return float('nan')

def specificity(TN, FP):
    """Calculates specificity (precision) from confusion matrix values.
    Proportion of actual negatives correctly identified.
    Args:
        TN (int): True Negatives.
        FP (int): False Positives."""
    
    # Validate inputs
    assert all(type(i) == int for i in [TN, FP]), "All inputs must be integers."
    assert all(i >= 0 for i in [TN, FP]), "All inputs must be equal or greater than 0."
    
    # Calculate and return specificity
    try:
        return TN / (TN + FP)
    except ZeroDivisionError:
        return float('nan')

def pos_pred_val(TP, FP):
    """Calculates positive predictive value from confusion matrix values.
    Probability that a data point predicted as positive is actually positive.
    Args:
        TP (int): True Positives.
        FP (int): False Positives."""
    
    # Validate inputs
    assert all(type(i) == int for i in [TP, FP]), "All inputs must be integers."
    assert all(i >= 0 for i in [TP, FP]), "All inputs must be equal or greater than 0."

    # Calculate and return positive predictive value
    try:
        return TP / (TP + FP)
    except ZeroDivisionError: 
        return float('nan')

def neg_pred_val(TN, FN):
    """Calculates negative predictive value from confusion matrix values.
    Probability that a data point predicted as negative is actually negative.
    Args:
        TN (int): True Negatives.
        FN (int): False Negatives."""
    
    # Validate inputs
    assert all(type(i) == int for i in [TN, FN]), "All inputs must be integers."
    assert all(i >= 0 for i in [TN, FN]), "All inputs must be equal or greater than 0."

    # Calculate and return negative predictive value
    try:
        return TN / (TN + FN)
    except ZeroDivisionError:
        return float('nan')

def print_eval_metrics(predicted, actual, positive = 1):
    """Prints evaluation metrics based on predicted and actual labels.
    Args:
        predicted(list): The predicted values from the model.
        actual (list): The list of actual/true values.
        positive (int|float|str): The class considered as positive."""
    
    assert type(predicted) == list, "Predicted values must be a list."
    assert type(actual) == list, "Actual/true values must be a list."
    assert len(predicted) == len(actual), "Predicted and actual values must have the same length."
    assert len(predicted) > 0, "Predicted and actual values must have at least one element."
    assert type(positive) == int or type(positive) == float or type(positive) == str, "Positive class must be an integer, float, or string."
    
    # Extract confusion matrix values
    TP, FP, TN, FN = confusion_matrix(predicted, actual, positive)
    
    # Calculate and print evaluation metrics
    print(f"Accuracy: {accuracy(TP, FP, TN, FN)}")
    print(f"Sensitivity (Recall): {sensitivity(TP, FN)}")
    print(f"Specificity (Precision): {specificity(TN, FP)}")
    print(f"Positive Predictive Value: {pos_pred_val(TP, FP):}")
    print(f"Negative Predictive Value: {neg_pred_val(TN, FN):}")

if __name__ == "__main__":
    main()