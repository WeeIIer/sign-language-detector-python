import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import time


data_dict = pickle.load(open('./data.pickle', 'rb'))
data = np.asarray(data_dict['data'], dtype=float)
labels = np.asarray(data_dict['labels'], dtype=str)

print("Обучение модели началось.")
start = time.time()

x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

model = RandomForestClassifier()

model.fit(x_train, y_train)

stop = time.time()
print(f"Модель обучена. Затрачено времени: {stop - start} сек.")

y_predict = model.predict(x_test)

score = accuracy_score(y_predict, y_test)
print(f"{score * 100}% образцов были классифицированы правильно!")

with open("model.pickle", "wb") as file:
    pickle.dump({"model": model}, file)
