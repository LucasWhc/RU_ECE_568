import numpy as np
import time

# In this neural network, there are two input units, two hidden units and one output unit
# I use back propagation and gradient descent

input_unit = 2
hidden_unit = 2
output_unit = 1
X = [[0, 0], [0, 1], [1, 0], [1, 1]]
Y = [[0], [1], [1], [0]]
# The size of training data
m = 4


# Logistic regression
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def gradient_of_sigmoid(z):
    return sigmoid(z) * (1 - sigmoid(z))


def init_weight(u1, u2):
    epsilon = np.sqrt(6) / np.sqrt(u1 + u2)
    seed = np.random.RandomState(int(round(time.time())))
    omega = seed.rand(u2, u1 + 1) * 2 * epsilon - epsilon
    return np.asarray(omega)


def set_network(theta1, theta2):
    # Setup the neural network with forward propagation
    a1 = X
    a1 = np.concatenate((np.ones((m, 1)), a1), axis=1)
    z2 = np.dot(np.asarray(a1), theta1.T)
    a2 = sigmoid(z2)
    a2 = np.concatenate((np.ones((m, 1)), a2), axis=1)
    z3 = np.dot(np.asarray(a2), theta2.T)
    a3 = sigmoid(z3)

    # Calculate the cost
    cost = np.asarray(Y) * np.log(a3) + (1 - np.asarray(Y)) * np.log(1 - a3)
    J = -np.sum(cost) / m

    # Use back propagation
    delta3 = a3 - np.asarray(Y)
    delta2 = (delta3 * theta2)[:, 2:] * gradient_of_sigmoid(z2)
    Delta1 = np.dot(delta2.T, a1)
    Delta2 = np.dot(delta3.T, a2)
    theta1_grad = Delta1 / m
    theta2_grad = Delta2 / m
    return J, theta1_grad, theta2_grad


# Train the network using gradient descent
def gradient_descent(learning_rate, target_error, theta1, theta2):
    J, theta1_grad, theta2_grad = set_network(theta1, theta2)
    cnt = 0
    while J >= target_error:
        theta1 = theta1 - theta1_grad * learning_rate
        theta2 = theta2 - theta2_grad * learning_rate
        J, theta1_grad, theta2_grad = set_network(theta1, theta2)
        cnt = cnt + 1
        # print(cnt)
    return J, theta1, theta2, cnt


# Predict the output
def predict(x, theta1, theta2):
    a1 = x
    a1 = np.concatenate((np.ones((m, 1)), a1), axis=1)
    z2 = np.dot(np.asarray(a1), theta1.T)
    a2 = sigmoid(z2)
    a2 = np.concatenate((np.ones((m, 1)), a2), axis=1)
    z3 = np.dot(np.asarray(a2), theta2.T)
    a3 = sigmoid(z3)
    return a3


def main():
    learning_rate = [0.05, 0.1, 0.25, 0.5, 0.8, 1]
    target_error = 0.08
    print("The target error is ", target_error)

    theta1_init = init_weight(input_unit, hidden_unit)
    theta2_init = init_weight(hidden_unit, output_unit)
    print("The initial weights of the neural network are ", theta1_init, " and ", theta2_init)

    for l_rate in learning_rate:
        print("The learning rate is ", l_rate)
        J, theta1, theta2, cnt = gradient_descent(l_rate, target_error, theta1_init, theta2_init)
        res = predict(X, theta1, theta2)
        print("The final weights are", theta1, " and ", theta2)
        print("The final error is ", J)
        print("The program runs ", cnt, " times to complete computing")
        print("The prediction of X is ", res)


if __name__ == "__main__":
    main()
