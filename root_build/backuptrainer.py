import pickle
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

data_dict = pickle.load((open('./data.pickle', 'rb')))
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()

# Lists to store accuracy and loss values during training
train_accuracy = []
test_accuracy = []

num_epochs = 10  # Set the number of epochs for training

for epoch in range(num_epochs):
    model.fit(x_train, y_train)

    # Calculate and store accuracy for training and testing data during each epoch
    train_accuracy.append(accuracy_score(y_train, model.predict(x_train)))
    test_accuracy.append(accuracy_score(y_test, model.predict(x_test)))

    print(f'Epoch {epoch + 1}/{num_epochs}: Test Accuracy: {test_accuracy[-1] * 100:.2f}%')

print('Training completed!')

# Plot accuracy
plt.plot(train_accuracy, label='Train Accuracy', color='blue', marker = 'o')
plt.plot(test_accuracy, label='Test Accuracy', color="green", marker = 'o')
plt.xlabel('Epochs (Cycles)')
plt.ylabel('Accuracy (%)')
plt.ylim(0.9, 1)  # Set the y-axis limits to enforce range from 0 to 1 (0% to 100%)
plt.legend()
plt.title('S.lang AI Training Accuracy')
plt.show()

# Save the final trained model
f = open('slangaitest.p', 'wb')
pickle.dump({'model': model}, f)
f.close()