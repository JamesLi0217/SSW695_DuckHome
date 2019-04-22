import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib

# Load clean data
df = pd.read_csv('../pre_data/clean_data.csv')

# Select factor and value columns
data = df[['bed', 'bath', 'square', 'city', 'price']]

# One Hot Encoder factors 'bed', 'bath', 'city'
# Save to new DataFrame data_one_hot
data_one_hot = pd.get_dummies(data[['bed', 'bath', 'city']])

# Connect data_one_hot with column 'square' and 'price'
new_data = pd.concat([data_one_hot, data[['square', 'price']]], axis=1)

# Normalize the square
new_data['square'] = new_data[['square']].apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))

# Split data into train data and test data with ratio 4:1
X = new_data.iloc[:, : -1]
y = new_data['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1 / 5, random_state=1)

# Build gradient descent method linear regression model
alphas = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3]
cv_scores = []
for a in alphas:
    SGD_model = SGDRegressor(alpha=a, loss='squared_loss')
    scores = cross_val_score(SGD_model, X_train, y_train, cv=10)
    cv_score = np.mean(scores)
    # print('alpha={}，R-squared score on train data={:.3f}'.format(a, cv_score))
    cv_scores.append(cv_score)

best_alpha = alphas[np.argmax(cv_scores)]
best_alpha = SGDRegressor(alpha=best_alpha, loss='squared_loss', random_state=1)
best_alpha.fit(X_train, y_train)

# Save model
model_path = './SGDRegression_model.pkl'
joblib.dump(best_alpha, model_path)

# Predict test
model = joblib.load('./SGDRegression_model.pkl')

# Predict
ex = np.array([1, 1, 1, 0, 0, 0.9])
predict = np.round(model.predict([ex])[0], 1)
print(predict)
