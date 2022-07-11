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
        - Administrative, an integer 0
        - Administrative_Duration, a floating point number 1
        - Informational, an integer 2
        - Informational_Duration, a floating point number 3
        - ProductRelated, an integer 4
        - ProductRelated_Duration, a floating point number 5
        - BounceRates, a floating point number 6
        - ExitRates, a floating point number 7
        - PageValues, a floating point number 8
        - SpecialDay, a floating point number 9
        - Month, an index from 0 (January) to 11 (December) 10
        - OperatingSystems, an integer 11
        - Browser, an integer 12
        - Region, an integer 13
        - TrafficType, an integer 14
        - VisitorType, an integer 0 (not returning) or 1 (returning) 15
        - Weekend, an integer 0 (if false) or 1 (if true) 16

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Opening the CSV
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        evidence = list()
        labels = list()
        for row in csv_reader:
            # Skipping the first row
            if line_count == 0: 
                line_count += 1
                continue

            # EVIDENCE AND LABELS LIST
            tmp_evidence = list()

            # Months List
            MONTHS = ['Jan', 'Feb', 'Mar', 'Apr','May', 'Jun', 'Jul', 'Aug', 'Sep','Oct', 'Nov', 'Dic']
          
            
            for i in range(len(row)):
                if (i == 0 or i == 2 or i == 4 or i == 11 or i == 12 or i == 13 or i == 14):
                    tmp_evidence.append(int(row[i]))
                elif i == 1 or i == 3 or i == 5 or i == 6 or i == 7 or i == 8 or i == 9:
                    tmp_evidence.append(float(row[i]))
                elif i == 15:
                    if row[i] == 'Returning_Visitor':
                        tmp_evidence.append(1)
                    else: 
                        tmp_evidence.append(0)
                elif i == 16:
                    if row[i] == "TRUE":
                        tmp_evidence.append(1)
                    else :
                        tmp_evidence.append(0)
                elif i == 17:
                    if row[i] == "TRUE":
                        labels.append(1)
                    else :
                        labels.append(0)
                elif i == 10:
                    for c, val in enumerate(MONTHS):
                        if row[10] == c:
                            tmp_evidence.append(int(val))
                        continue
            evidence.append(tmp_evidence)
            
        return evidence, labels

    

    

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    neigh = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence, labels)

    return neigh


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0.0
    specificity = 0.0

    i = 0
    sen_c = 0
    spe_c = 0
    for pre in predictions:
        if labels[i] == 1:
            if pre == 1:
                sensitivity += 1
            sen_c += 1
        elif labels[i] == 0:
            if pre == 0:
                specificity += 1
            spe_c += 1
        i += 1
    return (sensitivity/sen_c , specificity/spe_c)


if __name__ == "__main__":
    main()
