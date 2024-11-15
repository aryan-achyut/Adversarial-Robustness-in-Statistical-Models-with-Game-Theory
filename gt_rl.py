# -*- coding: utf-8 -*-
"""GT_RL.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1nOoaa92bBa1dOuIQMWvsR7q-lpTA76vI
"""

!pip install scikit-learn numpy torch

from sklearn.datasets import fetch_covtype
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# Load dataset
data = fetch_covtype()
X, y = data.data, data.target

# Binary classification: label as 1 for class 1, 0 for others
y = (y == 1).astype(int)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define classifier model
class Classifier(nn.Module):
    def __init__(self, input_size):
        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# Define adversary to create perturbations
class Adversary:
    def __init__(self, epsilon=0.1):
        self.epsilon = epsilon

    def attack(self, x):
        # Add small random noise
        perturbation = self.epsilon * torch.sign(torch.randn_like(x))
        return x + perturbation

# Initialize models
input_size = X_train.shape[1]
model = Classifier(input_size)
adversary = Adversary(epsilon=0.2)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Convert data to PyTorch tensors
X_train_tensor = torch.FloatTensor(X_train)
y_train_tensor = torch.FloatTensor(y_train).unsqueeze(1)
X_test_tensor = torch.FloatTensor(X_test)
y_test_tensor = torch.FloatTensor(y_test).unsqueeze(1)

# Training loop
epochs = 20
for epoch in range(epochs):
    model.train()

    # Adversarial attack
    X_adv = adversary.attack(X_train_tensor)

    # Forward pass with adversarial samples
    optimizer.zero_grad()
    outputs = model(X_adv)
    loss = criterion(outputs, y_train_tensor)

    # Backward pass and optimization
    loss.backward()
    optimizer.step()

    # Evaluate adversarial performance
    if (epoch + 1) % 5 == 0:
        model.eval()
        with torch.no_grad():
            y_pred = model(X_test_tensor)
            y_pred_labels = (y_pred > 0.5).float()
            acc = accuracy_score(y_test, y_pred_labels)
            auc = roc_auc_score(y_test, y_pred)
        print(f"Epoch {epoch + 1}, Loss: {loss.item():.4f}, Accuracy: {acc:.4f}, AUC: {auc:.4f}")

# Generate adversarial samples for test set
X_test_adv = adversary.attack(X_test_tensor)

# Evaluate model on adversarial samples
model.eval()
with torch.no_grad():
    y_test_pred = model(X_test_tensor)
    y_test_pred_adv = model(X_test_adv)

    # Standard test performance
    acc_standard = accuracy_score(y_test, (y_test_pred > 0.5).float())
    auc_standard = roc_auc_score(y_test, y_test_pred)

    # Adversarial test performance
    acc_adv = accuracy_score(y_test, (y_test_pred_adv > 0.5).float())
    auc_adv = roc_auc_score(y_test, y_test_pred_adv)

print(f"Standard Accuracy: {acc_standard:.4f}, Standard AUC: {auc_standard:.4f}")
print(f"Adversarial Accuracy: {acc_adv:.4f}, Adversarial AUC: {auc_adv:.4f}")
print(f"Accuracy Drop Due to Adversarial Attack: {acc_standard - acc_adv:.4f}")