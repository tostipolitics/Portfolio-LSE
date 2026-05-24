# Import modules
import unittest
import math
import class_eval

def main():
    pass

class TestSplitTrainingTesting(unittest.TestCase):
    """Tests for split_training_testing."""

    def test_split_training_testing_list_small(self):
        """Test a small list."""
        inputted = [1, 0]
        
        train_set, test_set = class_eval.split_training_testing(inputted)
        self.assertEqual(len(train_set) + len(test_set), len(inputted), "The list is a small list.")

    def test_split_training_testing_list_regular(self):
        """Test a regular list."""
        inputted = [1, 0, 1, 0, 0, 1]
        
        train_set, test_set = class_eval.split_training_testing(inputted)
        self.assertEqual(len(train_set) + len(test_set), len(inputted), "The list is a regular list.")
    
    def test_split_training_testing_list_long(self):
        """Test a long list."""
        inputted = [1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1]

        train_set, test_set = class_eval.split_training_testing(inputted)
        self.assertEqual(len(train_set) + len(test_set), len(inputted), "The list is a long list.")

    def test_split_training_testing_list_of_lists_small(self):
        """Test a small list of lists."""
        inputted = [["Cat", 50, 1, "Black"],
                    ["Dog", 35, 0, "White"]]

        train_set, test_set = class_eval.split_training_testing(inputted)
        self.assertEqual(len(train_set) + len(test_set), len(inputted), "The list is a regular list of lists.")

    def test_split_training_testing_list_of_lists_regular(self):
        """Test a regular list of lists."""
        inputted = [["Cat", 50, 1, "Black"],
                    ["Dog", 35, 0, "White"],
                    ["Cat", 55, 1, "White"],
                    ["Cat", 40, 1, "Black"],
                    ["Dog", 45, 0, "Black"]]

        train_set, test_set = class_eval.split_training_testing(inputted)
        self.assertEqual(len(train_set) + len(test_set), len(inputted), "The list is a regular list of lists.")
    
    def test_split_training_testing_list_of_lists_long(self):
        """Test a long list of lists."""
        inputted = [["Cat", 50, 1, "Black"],
                    ["Dog", 35, 0, "White"],
                    ["Cat", 55, 1, "White"],
                    ["Cat", 40, 1, "Black"],
                    ["Dog", 45, 0, "Black"],
                    ["Cat", 50, 1, "Black"],
                    ["Dog", 35, 0, "White"],
                    ["Cat", 55, 1, "White"],
                    ["Cat", 40, 1, "Black"],
                    ["Dog", 45, 0, "Black"],
                    ["Cat", 50, 1, "Black"],
                    ["Dog", 35, 0, "White"],
                    ["Cat", 55, 1, "White"],
                    ["Cat", 40, 1, "Black"],
                    ["Dog", 45, 0, "Black"]]
        
        train_set, test_set = class_eval.split_training_testing(inputted)
        self.assertEqual(len(train_set) + len(test_set), len(inputted), "The list is a regular list of lists.")
    
    def test_split_training_testing_complete(self):
        """Tests that train and test effectively contains all data according to unique values."""
        inputted = list(range(0, 100))
        train_set, test_set = class_eval.split_training_testing(inputted)
        self.assertTrue(set(train_set).isdisjoint(set(test_set)), "Train and test sets are complete.")
    
    def test_split_training_testing_ptest(self):
        """Test different p_test values."""
        inputted = [1, 0, 1, 0, 0, 1]

        for i in range(1, 100):
            train_set, test_set = class_eval.split_training_testing(inputted, p_test = i)
            self.assertEqual(len(train_set) + len(test_set), len(inputted), "Train and test sets are complete.")

    
class TestConfusionMatrix(unittest.TestCase):
    """Tests for confusion_matrix."""

    def test_confusion_matrix_int(self):
        pred = [0, 1, 0, 0, 1, 1]
        y =    [0, 0, 1, 0, 1, 0]
        n = len(y)

        # Confusion matrix
        for i in [0, 1]:
            TP, FP, TN, FN = class_eval.confusion_matrix(predicted =  pred, actual = y, positive = i)
            n_matrix = TP + FP + TN + FN
            
            # Evaluate if confusion matrix has all the elements
            self.assertEqual(n, n_matrix, 'Confussion matrix if the class is an integer.')
    
    def test_confusion_matrix_float(self):
        pred = [0.5, 1.5, 0.5, 0.5, 1.5, 1.5]
        y =    [0.5, 0.5, 1.5, 0.5, 1.5, 0.5]
        n = len(y)

        # Confusion matrix
        for i in [0.5, 1.5]:
            TP, FP, TN, FN = class_eval.confusion_matrix(predicted =  pred, actual = y, positive = i)
            n_matrix = TP + FP + TN + FN
            
            # Evaluate if confusion matrix has all the elements
            self.assertEqual(n, n_matrix, 'Confussion matrix if the class is a float.')

    def test_confusion_matrix_str(self):
        pred = ['Democrat', 'Republican', 'Republican', 'Republican', 'Republican', 'Democrat']
        y =    ['Democrat', 'Democrat', 'Republican', 'Democrat', 'Republican', 'Democrat']
        n = len(y)

        # Confusion matrix
        for i in [0, 1]:
            TP, FP, TN, FN = class_eval.confusion_matrix(predicted =  pred, actual = y, positive = i)
            n_matrix = TP + FP + TN + FN
            
            # Evaluate if confusion matrix has all the elements
            self.assertEqual(n, n_matrix, 'Confussion matrix if the class is a string.')
    
    def test_confusion_matrix_one_element(self):
        """Test a case with one element."""
        for pred, y in [[1, 1], [0, 0], [1, 0], [0, 1]]:
            TP, FP, TN, FN = class_eval.confusion_matrix(predicted =  [pred], actual = [y], positive = 1)
            
            # Evaluate if confusion matrix is correct
            if pred == 1 and y == 1:
                self.assertEqual(1, TP, 'Confussion matrix with one element.')
            elif pred == 0 and y == 0:
                self.assertEqual(1, TN, 'Confussion matrix with one element.')
            elif pred == 1 and y == 0:
                self.assertEqual(1, FP, 'Confussion matrix with one element.')
            elif pred == 0 and y == 1:
                self.assertEqual(1, FN, 'Confussion matrix with one element.')
    
    def test_confusion_matrix_all_correct(self):
        """Test a case where all predictions are correct."""
        pred = [1, 0, 1, 0, 1]
        y =    [1, 0, 1, 0, 1]
        n = len(y)

        for i in [0, 1]:
            TP, FP, TN, FN = class_eval.confusion_matrix(predicted =  pred, actual = y, positive = i)
            
            # Evaluate if all predictions are correct
            self.assertEqual(n, TP + TN, 'Confussion matrix when all predictions are correct.')
            self.assertEqual(0, FP, 'Confussion matrix when all predictions are correct.')
            self.assertEqual(0, FN, 'Confussion matrix when all predictions are correct.')
    
    def test_confusion_matrix_all_incorrect(self):
        """Test a case where all predictions are incorrect."""
        pred = [1, 1, 0, 0, 1]
        y =    [0, 0, 1, 1, 0]
        n = len(y)

        for i in [0, 1]:
            TP, FP, TN, FN = class_eval.confusion_matrix(predicted =  pred, actual = y, positive = i)
            
            # Evaluate if all predictions are incorrect
            self.assertEqual(n, FP + FN, 'Confussion matrix when all predictions are incorrect.')
            self.assertEqual(0, TP, 'Confussion matrix when all predictions are incorrect.')
            self.assertEqual(0, TN, 'Confussion matrix when all predictions are incorrect.')
    
class TestAccuracy(unittest.TestCase):
    """Tests for accuracy."""

    def test_accuracy_zero(self):
        """Test a zero accuracy."""
        TP, FP, TN, FN = 0, 50, 0, 50
        acc = class_eval.accuracy(TP, FP, TN, FN)
        self.assertEqual(0, acc, "Zero accuracy.")
    
    def test_accuracy_half(self):
        """Test a half accuracy."""
        TP, FP, TN, FN = 25, 25, 25, 25
        acc = class_eval.accuracy(TP, FP, TN, FN)
        self.assertEqual(0.5, acc, "Half accuracy.")

    def test_accuracy_perfect(self):
        """Test a perfect accuracy."""
        TP, FP, TN, FN = 50, 0, 50, 0
        acc = class_eval.accuracy(TP, FP, TN, FN)
        self.assertEqual(1, acc, "Perfect accuracy.")
    
    def test_accuracy_nan(self):
        """Test a NaN accuracy."""
        TP, FP, TN, FN = 0, 0, 0, 0
        acc = class_eval.accuracy(TP, FP, TN, FN)
        self.assertTrue(math.isnan(acc), "NaN accuracy.")
    
    def test_accuracy_negative_inputs(self):
        """Test that negative inputs raise an AssertionError."""
        with self.assertRaises(AssertionError):
            class_eval.accuracy(-1, 2, 3, -4)

    def test_accuracy_large_inputs(self):
        """Test accuracy with large inputs."""
        TP, FP, TN, FN = 11**50, 0, 30**15, 0
        acc = class_eval.accuracy(TP, FP, TN, FN)
        self.assertEqual(1, acc, "Accuracy with large inputs.")

class TestSensitivity(unittest.TestCase):
    """Tests for sensitivity."""

    def test_sensitivity_zero(self):
        """Test a zero sensitivity."""
        TP, FN = 0, 50
        sens = class_eval.sensitivity(TP, FN)
        self.assertEqual(0, sens, "Zero sensitivity.")
    
    def test_sensitivity_half(self):
        """Test a half sensitivity."""
        TP, FN = 25, 25
        sens = class_eval.sensitivity(TP, FN)
        self.assertEqual(0.5, sens, "Half sensitivity.")

    def test_sensitivity_perfect(self):
        """Test a perfect sensitivity."""
        TP, FN = 50, 0
        sens = class_eval.sensitivity(TP, FN)
        self.assertEqual(1, sens, "Perfect sensitivity.")
    
    def test_sensitivity_nan(self):
        """Test a NaN sensitivity."""
        TP, FN = 0, 0
        sens = class_eval.sensitivity(TP, FN)
        self.assertTrue(math.isnan(sens), "NaN sensitivity.")
    
    def test_sensitivity_negative_inputs(self):
        """Test that negative inputs raise an AssertionError."""
        with self.assertRaises(AssertionError):
            class_eval.sensitivity(-1, -2)

class TestSpecificity(unittest.TestCase):
    """Tests for specificity."""

    def test_specificity_zero(self):
        """Test a zero specificity."""
        TN, FP = 0, 50
        spec = class_eval.specificity(TN, FP)
        self.assertEqual(0, spec, "Zero specificity.")
    
    def test_specificity_half(self):
        """Test a half specificity."""
        TN, FP = 25, 25
        spec = class_eval.specificity(TN, FP)
        self.assertEqual(0.5, spec, "Half specificity.")

    def test_specificity_perfect(self):
        """Test a perfect specificity."""
        TN, FP = 50, 0
        spec = class_eval.specificity(TN, FP)
        self.assertEqual(1, spec, "Perfect specificity.")
    
    def test_specificity_nan(self):
        """Test a NaN specificity."""
        TN, FP = 0, 0
        spec = class_eval.specificity(TN, FP)
        self.assertTrue(math.isnan(spec), "NaN specificity.")
    
    def test_specificity_negative_inputs(self):
        """Test that negative inputs raise an AssertionError."""
        with self.assertRaises(AssertionError):
            class_eval.specificity(-1, -2)

class TestPosPredVal(unittest.TestCase):
    """Tests for positive predictive value."""

    def test_pos_pred_val_zero(self):
        """Test a zero positive predictive value."""
        TP, FP = 0, 50
        ppv = class_eval.pos_pred_val(TP, FP)
        self.assertEqual(0, ppv, "Zero positive predictive value.")
    
    def test_pos_pred_val_half(self):
        """Test a half positive predictive value."""
        TP, FP = 25, 25
        ppv = class_eval.pos_pred_val(TP, FP)
        self.assertEqual(0.5, ppv, "Half positive predictive value.")

    def test_pos_pred_val_perfect(self):
        """Test a perfect positive predictive value."""
        TP, FP = 50, 0
        ppv = class_eval.pos_pred_val(TP, FP)
        self.assertEqual(1, ppv, "Perfect positive predictive value.")
    
    def test_pos_pred_val_nan(self):
        """Test a NaN positive predictive value."""
        TP, FP = 0, 0
        ppv = class_eval.pos_pred_val(TP, FP)
        self.assertTrue(math.isnan(ppv), "NaN positive predictive value.")
    
    def test_pos_pred_val_negative_inputs(self):
        """Test that negative inputs raise an AssertionError."""
        with self.assertRaises(AssertionError):
            class_eval.pos_pred_val(-1, -2)

class TestNegPredVal(unittest.TestCase):
    """Tests for negative predictive value."""

    def test_neg_pred_val_zero(self):
        """Test a zero negative predictive value."""
        TN, FN = 0, 50
        npv = class_eval.neg_pred_val(TN, FN)
        self.assertEqual(0, npv, "Zero negative predictive value.")
    
    def test_neg_pred_val_half(self):
        """Test a half negative predictive value."""
        TN, FN = 25, 25
        npv = class_eval.neg_pred_val(TN, FN)
        self.assertEqual(0.5, npv, "Half negative predictive value.")

    def test_neg_pred_val_perfect(self):
        """Test a perfect negative predictive value."""
        TN, FN = 50, 0
        npv = class_eval.neg_pred_val(TN, FN)
        self.assertEqual(1, npv, "Perfect negative predictive value.")
    
    def test_neg_pred_val_nan(self):
        """Test a NaN negative predictive value."""
        TN, FN = 0, 0
        npv = class_eval.neg_pred_val(TN, FN)
        self.assertTrue(math.isnan(npv), "NaN negative predictive value.")
    
    def test_neg_pred_val_negative_inputs(self):
        """Test that negative inputs raise an AssertionError."""
        with self.assertRaises(AssertionError):
            class_eval.neg_pred_val(-1, -2)
    
if __name__ == '__main__':
    unittest.main()