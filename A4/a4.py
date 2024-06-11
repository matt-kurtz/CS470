# Assignment 4
# By: Matthew Kurtz
# CS470 - Artificial Intelligence SU24

import pandas as pd
import numpy as np
from collections import Counter
import math
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Load the dataset
file_path = 'decisiontreedata.CSV'
data = pd.read_csv(file_path)

# Separate features and target
features = data.drop(['Example', 'Decision'], axis=1)
target = data['Decision']

# Define functions for entropy and information gain
def entropy(s):
    # Calculate entropy of a list of values
    counts = Counter(s)
    probabilities = [count / len(s) for count in counts.values()]
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def information_gain(data, split_attribute_name, target_name='Decision'):
    # Calculate the total entropy of the dataset
    total_entropy = entropy(data[target_name])
    
    # Calculate the values and counts for the split attribute
    vals, counts = np.unique(data[split_attribute_name], return_counts=True)
    
    # Calculate the weighted entropy
    weighted_entropy = sum((counts[i] / np.sum(counts)) * entropy(data.where(data[split_attribute_name]==vals[i]).dropna()[target_name]) for i in range(len(vals)))
    
    # Calculate information gain
    information_gain = total_entropy - weighted_entropy
    return information_gain

def id3(data, originaldata, features, target_attribute_name='Decision', parent_node_class=None):
    # Define stopping criteria
    
    # If all target values have the same value, return this value
    if len(np.unique(data[target_attribute_name])) <= 1:
        return np.unique(data[target_attribute_name])[0]
    
    # If the dataset is empty, return the mode target feature value in the original dataset
    elif len(data) == 0:
        return np.unique(originaldata[target_attribute_name])[np.argmax(np.unique(originaldata[target_attribute_name], return_counts=True)[1])]
    
    # If the feature space is empty, return the mode target feature value of the parent node
    elif len(features) == 0:
        return parent_node_class
    
    # If none of the above holds true, grow the tree
    else:
        # Set the default value for this node
        parent_node_class = np.unique(data[target_attribute_name])[np.argmax(np.unique(data[target_attribute_name], return_counts=True)[1])]
        
        # Select the feature which best splits the dataset
        item_values = [information_gain(data, feature, target_attribute_name) for feature in features]
        best_feature_index = np.argmax(item_values)
        best_feature = features[best_feature_index]
        
        # Create the tree structure
        tree = {best_feature: {}}
        
        # Remove the feature with the best information gain
        features = [i for i in features if i != best_feature]
        
        # Grow a branch under the root node for each possible value of the split attribute
        for value in np.unique(data[best_feature]):
            value = value
            sub_data = data.where(data[best_feature] == value).dropna()
            subtree = id3(sub_data, data, features, target_attribute_name, parent_node_class)
            tree[best_feature][value] = subtree
        
        return tree

def predict(query, tree, default=1):
    # Predict the class label for a single query using the decision tree
    for key in query.keys():
        if key in tree:
            try:
                result = tree[key][query[key]]
            except KeyError:
                return default

            if isinstance(result, dict):
                return predict(query, result)
            else:
                return result
    return default

def test(data, tree):
    # Test the decision tree on the given test data
    queries = data.iloc[:,:-1].to_dict(orient="records")
    predicted = pd.DataFrame(columns=["predicted"]) 

    for i in range(len(data)):
        predicted.loc[i, "predicted"] = predict(queries[i], tree, 1) 

    predicted.index = data.index  # Align indices
    accuracy = (np.sum(predicted["predicted"] == data["Decision"]) / len(data)) * 100
    print('The prediction accuracy is: ', accuracy, '%')

# Split data into training and test sets
train_data, test_data = train_test_split(data, test_size=0.3, random_state=42)

# Train the tree
tree = id3(train_data, train_data, train_data.columns[1:-1])

# Test the tree
test(test_data, tree)

# Experiment with different training sizes
def evaluate_decision_tree(data, target, training_sizes):
    accuracies = []
    for size in training_sizes:
        # Split the data into training and test sets based on the given size
        X_train, X_test, y_train, y_test = train_test_split(data, target, train_size=size/len(data), random_state=42)
        train_data = pd.concat([X_train, y_train], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)
        
        # Train the tree on the training data
        tree = id3(train_data, train_data, train_data.columns[1:-1])
        
        # Test the tree on the test data
        queries = test_data.iloc[:,:-1].to_dict(orient="records")
        predicted = pd.DataFrame(columns=["predicted"]) 
        for i in range(len(test_data)):
            predicted.loc[i, "predicted"] = predict(queries[i], tree, 1) 
        predicted.index = test_data.index  # Align indices
        accuracy = (np.sum(predicted["predicted"] == test_data["Decision"]) / len(test_data))
        accuracies.append(accuracy)
    return accuracies

# Define the different training sizes
training_sizes = [2, 5, 10, 20, 50, 99]

# Evaluate the decision tree
accuracies = evaluate_decision_tree(features, target, training_sizes)

print(accuracies)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(training_sizes, accuracies, marker='o')
plt.title('Decision Tree Accuracy vs Training Size')
plt.xlabel('Training Size')
plt.ylabel('Accuracy')
plt.grid(True)
plt.show()
