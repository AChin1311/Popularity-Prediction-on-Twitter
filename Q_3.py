import json
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn import metrics
from sklearn.metrics import make_scorer, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor

data = np.zeros((99999999, 5))

with open("tweets_#patriots.txt") as f:
    tweets = f.readlines()
    print(len(tweets))
    nums = 0
    for t in tweets:
        tw = json.loads(t)
        if tw['type'] == 'tweet':
            data[nums][0] = tw['author']['followers']
            data[nums][1] = tw['metrics']['impressions']
            data[nums][2] = tw['metrics']['citations']['influential']
            data[nums][3] = int(tw['tweet']['created_at'][11:13])
            data[nums][4] = tw['metrics']['citations']['total']
            nums += 1
    print(nums)


data = data[:nums].astype(np.uint32)
np.random.shuffle(data)

X = data[:,:-1]
Y = data[:,-1]


#random forest
c = 0.1

num_trees = np.arange(1,17) * 3
num_features = list(range(1,4))
num_depths = list(range(3,7))

min_rmse_index = []
plt.figure()
for ndepths in num_depths:
  rmse = []
  for ntrees in num_trees:  
    print("Doing rmse - depths: ", ndepths, ", trees: ", ntrees)  
    test_mse =[]
    train_mse =[]
    kf = KFold(n_splits=10, random_state=None, shuffle=False)
    for train_index, test_index in kf.split(X):
      X_train, X_test = X[train_index], X[test_index]
      Y_train, Y_test = Y[train_index], Y[test_index]
      train_size = X_train.shape[0]
      test_size = X_test.shape[0]
      regr = RandomForestRegressor(n_estimators=ntrees, max_depth=ndepths, max_features= 4, n_jobs=-1)
      regr.fit(X_train, Y_train)
      Y_test_predict = regr.predict(X_test)
      test_mse.append(mean_squared_error(Y_test, Y_test_predict))
    rmse.append(np.sqrt(np.mean(test_mse)))

  min_rmse_index.append(rmse.index(min(rmse)))

  y = rmse
  x = num_trees
  plt.plot(x, y, lw=2, label="# of depths = "+str(ndepths))
  plt.grid(color=str(c), linestyle='--', linewidth=1)
  c = c + 0.1
plt.xlabel('# of trees')
plt.ylabel('RMSE')
plt.legend()


#polynomial
num_orders = list(range(1,8))

plt.figure()
rmse = []
for order in num_orders:
    print("Doing rmse - order: ", order)  
    test_mse =[]
    train_mse =[]
    kf = KFold(n_splits=10, random_state=None, shuffle=False)
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        train_size = X_train.shape[0]
        test_size = X_test.shape[0]
        poly = PolynomialFeatures(order)
        X_train = poly.fit_transform(X_train)
        X_test = poly.fit_transform(X_test)
        model = linear_model.Ridge(alpha=1)
        model.fit(X_train,Y_train)
        #regr = RandomForestRegressor(n_estimators=ntrees, max_depth=ndepths, max_features= 4, n_jobs=-1)
        #regr.fit(X_train, Y_train)
        Y_test_predict = model.predict(X_test)
        test_mse.append(mean_squared_error(Y_test, Y_test_predict))
    tmp = np.sqrt(np.mean(test_mse))
    print(tmp)
    rmse.append(tmp)

y = rmse
x = num_orders
plt.plot(x, y, lw=2)
plt.grid(linestyle='--', linewidth=1)
plt.yscale('log')    
plt.xlabel('# of order')
plt.ylabel('RMSE')
plt.savefig('plot/3-RMSE-poly-superbowl.png')
plt.clf()
plt.savefig('plot/3-RMSE-randomforrest-patriots.png')
plt.clf()