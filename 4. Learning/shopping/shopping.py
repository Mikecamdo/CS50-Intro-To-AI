import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence, labels = [ ], [ ]

    with open(filename, 'r') as file:
        data = csv.reader(file)

        next(data) # skips the title row of the CSV file

        months = {
            'Jan': 0,
            'Feb': 1,
            'Mar': 2,
            'Apr': 3,
            'May': 4,
            'June': 5,
            'Jul': 6,
            'Aug': 7,
            'Sep': 8,
            'Oct': 9,
            'Nov': 10,
            'Dec': 11
        }

        for row in data:
            current_evidence = [ ]

            for i in range(17):
                if i == 1 or i == 3 or 5 <= i <= 9: # float columns (converting the string to a float)
                    current_evidence.append(float(row[i]))
                elif i == 10: # the Month column
                    current_evidence.append(months[row[i]]) # months['Feb'] = 1, months['Mar'] = 2, ...
                elif i == 15: # the VisitorType column
                    current_evidence.append(1 if row[i] == 'Returning_Visitor' else 0)
                elif i == 16: # the Weekend column
                    current_evidence.append(1 if row[i] == 'TRUE' else 0)
                else: # int columns (converting the string to an int)
                    current_evidence.append(int(row[i]))
            
            evidence.append(current_evidence)
            labels.append(1 if row[17] == 'TRUE' else 0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity, specificity = 0.0, 0.0

    true_positive_count = 0
    false_positive_count = 0

    true_negative_count = 0
    false_negative_count = 0

    for actual, predicted in zip(labels, predictions):
        if actual == predicted:
            if predicted == 0: # true negative
                true_negative_count += 1
            else: # true positive
                true_positive_count += 1
        else:
            if predicted == 0:
                false_negative_count += 1
            else:
                false_positive_count += 1

    sensitivity = true_positive_count / (true_positive_count + false_negative_count)
    specificity = true_negative_count / (true_negative_count + false_positive_count)

    return sensitivity, specificity


if __name__ == "__main__":
    main()
