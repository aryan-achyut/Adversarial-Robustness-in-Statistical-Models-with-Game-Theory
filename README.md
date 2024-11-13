# Adversarial Robustness in Statistical Models with Game Theory

This repository explores **adversarial robustness** in statistical models by applying **game-theoretic adversarial training**. Using PyTorch, we simulate a zero-sum game where a model (defender) and adversary iteratively compete, enhancing the model's resilience against adversarial attacks. This approach is particularly relevant for applications in **finance, healthcare,** and **cybersecurity**.

## Project Overview

- **Objective**: Train a model to withstand adversarial noise by treating training as a game between the model (defender) and adversarial attacker.
- **Approach**: Implemented a GAN-inspired setup where the adversary introduces perturbations to maximize model error, and the model adapts to minimize it.
- **Results**: Evaluated on standard and adversarial metrics (accuracy, AUC), showing resilience under attack.

## Code Summary

The code is organized as follows:

1. **Data Loading and Preprocessing**:
   - Uses `scikit-learn`'s `fetch_covtype` dataset for binary classification.
   - Preprocesses data by standardizing features for stable training.

2. **Model Architecture**:
   - A two-layer neural network classifier built with PyTorch.

3. **Adversarial Attack**:
   - Defined with adjustable noise level (epsilon) to simulate adversarial perturbations.

4. **Training Loop**:
   - Each epoch includes an adversarial attack on the training data, followed by a forward pass, loss calculation, and optimization step.
   - Outputs accuracy and AUC every 5 epochs for progress tracking.

5. **Evaluation**:
   - Assesses the model on both clean and adversarially perturbed test sets.
   - Measures accuracy drop due to adversarial attacks to evaluate model robustness.

## Results

| Metric                     | Standard Performance | Adversarial Performance | Accuracy Drop |
|----------------------------|----------------------|-------------------------|---------------|
| **Accuracy**               | 0.7081              | 0.7050                 | 0.0031        |
| **AUC**                    | 0.7745              | 0.7681                 | -            |

These results demonstrate that our adversarial training method helps the model retain stability under adversarial attacks with minimal performance drop.

## Requirements

- Python 3.7+
- Required libraries:
  ```bash
  pip install scikit-learn numpy torch
