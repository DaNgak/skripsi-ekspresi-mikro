import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict, GridSearchCV, KFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

class SVMClassifier:
    def __init__(self, dataset_file, label_column, feature_column=None, except_feature_column=None):
        self.dataset_file = dataset_file
        self.feature_column = feature_column
        self.except_feature_column = except_feature_column
        self.label_column = label_column
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.kf = None 
        self.label_encoder = LabelEncoder()

    def load_data(self):
        data = pd.read_csv(self.dataset_file)
        print(self.dataset_file)
        
        if self.feature_column is None and (self.except_feature_column is None or self.except_feature_column == [None]):
            raise ValueError("The 'feature_column' and 'except_feature_column' parameters are both empty. One of them must be provided.")
        
        if self.except_feature_column is not None and self.except_feature_column != [None]:
            self.X = data.drop(self.except_feature_column, axis=1).values
        elif self.feature_column is not None:
            self.X = data[self.feature_column].values
        
        # self.y = LabelEncoder().fit_transform(data[self.label_column].values)  # Encode label
        self.y = self.label_encoder.fit_transform(data[self.label_column].values)  # Encode label

    def split_data(self, test_size=0.2, random_state=42):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=test_size, random_state=random_state
        )

        # Feature scaling
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)

    def train_model(self, C=1, kernel='linear', gamma='scale', autoParams=False):
        if autoParams:
            # Low Range: 0.01, 0.1, 1
            # Medium Range: 1, 10, 100
            # High Range: 10, 100, 1000
            param_grid = {
                'C': [0.01, 0.1, 1],
                'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                'gamma': ['scale', 'auto']
            }
            # Menggunakan GridSearchCV
            # grid_search = GridSearchCV(SVC(), param_grid, cv=5, scoring='accuracy')
            # grid_search.fit(self.X_train, self.y_train)
            # self.model = grid_search.best_estimator_
            # print(f"Best parameters Grid Search: {grid_search.best_params_}")

            # Menggunakan Kombinasi Manual
            best_params = {
                "combination": {},
                "accuracy": 0
            }

            for C in param_grid['C']:
                for kernel in param_grid['kernel']:
                    for gamma in param_grid['gamma']:
                        # print(f"Evaluating combination: C={C}, kernel={kernel}, gamma={gamma}")
                        model = SVC(C=C, kernel=kernel, gamma=gamma)
                        model.fit(self.X_train, self.y_train)
                        predictions = model.predict(self.X_test)
                        accuracy = accuracy_score(self.y_test, predictions)
                        # print(f"Accuracy for combination C={C}, kernel={kernel}, gamma={gamma}: {accuracy}")

                        if accuracy > best_params["accuracy"] and accuracy != 1:
                            best_params["combination"] = {'C': C, 'kernel': kernel, 'gamma': gamma}
                            best_params["accuracy"] = accuracy

            print("\nBest combination found:")
            print(best_params["combination"])
            print(f"Best accuracy: {best_params['accuracy']}")

            # Train the model with the best parameters
            self.model = SVC(**best_params["combination"])
            self.model.fit(self.X_train, self.y_train)
        else:
            print("C:", C, "Kernel:", kernel, "Gamma:", gamma)
            self.model = SVC(C=C, kernel=kernel, gamma=gamma)
            self.model.fit(self.X_train, self.y_train)
        
    # def train_model_cross_validation(self, param_grid=None, cv=10):
    #     if param_grid is None:
    #         param_grid = {
    #             'C': [0.01, 0.1, 1],
    #             'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
    #             'gamma': ['scale', 'auto']
    #         }
        
    #     grid_search = GridSearchCV(SVC(), param_grid, cv=cv, scoring='accuracy')
    #     grid_search.fit(self.X, self.y)  # Menggunakan seluruh dataset

    #     self.model = grid_search.best_estimator_
        
    #     print(f"Best parameters found: {grid_search.best_params_}")
    #     print(f"Best cross-validation accuracy: {grid_search.best_score_}")
    
    def train_model_cross_validation(self, param_grid=None, cv=10, random_state=42):
        if param_grid is None:
            param_grid = {
                'C': [0.01, 0.1, 1],
                'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
                'gamma': ['scale', 'auto']
            }

        self.kf = KFold(n_splits=cv, shuffle=True, random_state=random_state)
        
        grid_search = GridSearchCV(SVC(), param_grid, cv=self.kf, scoring='accuracy')
        grid_search.fit(self.X, self.y)

        self.model = grid_search.best_estimator_
        
        print(f"Best parameters found: {grid_search.best_params_}")
        print(f"Best cross-validation accuracy: {grid_search.best_score_}")

    def evaluate_model(self):
        predictions = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, predictions)
        cm = confusion_matrix(self.y_test, predictions)
        
        print("Accuracy:", accuracy)
        print("\nConfusion Matrix:")
        print(cm)

        # Display the confusion matrix with proper formatting
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=self.label_encoder.classes_, yticklabels=self.label_encoder.classes_)
        plt.xlabel("Predicted labels")
        plt.ylabel("True labels")
        plt.title("Confusion Matrix")
        plt.show()

    # def evaluate_model_cross_validation(self, cv=10, random_state=42):
    #     kf = KFold(n_splits=cv, shuffle=True, random_state=random_state)
    #     accuracies = []

    #     for train_index, test_index in kf.split(self.X):
    #         X_train, X_test = self.X[train_index], self.X[test_index]
    #         y_train, y_test = self.y[train_index], self.y[test_index]
            
    #         # Feature scaling
    #         scaler = StandardScaler()
    #         X_train = scaler.fit_transform(X_train)
    #         X_test = scaler.transform(X_test)
            
    #         # Train the model
    #         self.model.fit(X_train, y_train)
            
    #         # Predict and evaluate
    #         predictions = self.model.predict(X_test)
    #         accuracy = accuracy_score(y_test, predictions)
    #         accuracies.append(accuracy)

    #     average_accuracy = np.mean(accuracies)

    #     print(f"Accuracy with {cv}-Fold Cross Validation: ")
    #     print(accuracies)
    #     print(f"Average Accuracy with {cv}-Fold Cross Validation: {average_accuracy:.2f}")

    def evaluate_model_cross_validation(self):
        # kf = KFold(n_splits=cv, shuffle=True, random_state=random_state)
        # scores = cross_val_score(self.model, self.X, self.y, cv=kf, scoring='accuracy')
        # print(f"Cross-validation accuracy scores: {scores}")
        # print(f"Mean cross-validation accuracy: {scores.mean()}")

        predictions = cross_val_predict(self.model, self.X, self.y, cv=self.kf)
        
        accuracy = accuracy_score(self.y, predictions)
        cm = confusion_matrix(self.y, predictions)
        
        print("Cross-validated Accuracy:", accuracy)
        print("\nConfusion Matrix:")
        print(cm)

        # Display the confusion matrix with proper formatting
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=self.label_encoder.classes_, yticklabels=self.label_encoder.classes_)
        plt.xlabel("Predicted labels")
        plt.ylabel("True labels")
        plt.title("Confusion Matrix")
        plt.show()

    def save_model(self, filename='svm_model.joblib', label_encoder_filename='label_encoder.joblib'):
        output_model_path = 'models'
        if not os.path.exists(output_model_path):
            os.makedirs(output_model_path)
        joblib.dump(self.model, os.path.join(output_model_path, filename))
        joblib.dump(self.label_encoder, os.path.join(output_model_path, label_encoder_filename)) 