import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import datetime
pd.set_option('display.max_columns', None)
from sklearn.cross_validation import KFold
from sklearn.cross_validation import train_test_split
import xgboost as xgb
from operator import itemgetter
import time
from sklearn import preprocessing


def write_to_csv(output,score):
    now = datetime.datetime.now()
    sub_file = 'submission_' + str(score) + '_' + str(now.strftime("%Y-%m-%d-%H-%M")) + '.csv'
    print('Writing submission: ', sub_file)
    f = open(sub_file, 'w')
    prediction_file_object = csv.writer(f)
    prediction_file_object.writerow(["zpid","price"])  # don't forget the headers

    for i in range(len(test)):
        prediction_file_object.writerow([test["zpid"][test.index[i]], (output[i])])

def get_features(train, test):
    trainval = list(train.columns.values) # list train features
    testval = list(test.columns.values) # list test features
    output = list(set(trainval) & set(testval)) # check wich features are in common (remove the outcome column)
    output.remove('zpid') # remove non-usefull id column
    return output


def process_features(train, test):
    tables = [test, train]
    print("Handling missing values...")
    total_missing = train.isnull().sum()
    to_delete = total_missing[total_missing > (1460 / 3.)]  # select features with more than 1/3 missing values
    for table in tables:
        table.drop(to_delete.index.tolist(), axis=1, inplace=True)

    print("Filling Nan...")
    numerical_features = test.select_dtypes(include=["float", "int", "bool"]).columns.values
    categorical_features = train.select_dtypes(include=["object"]).columns.values
    for table in tables:
        for feature in numerical_features:
            table[feature].fillna(train[feature].median(), inplace=True)  # replace by median value
        for feature in categorical_features:
            table[feature].fillna(train[feature].value_counts().idxmax(),
                                  inplace=True)  # replace by most frequent value

    print("Handling categorical features...")
    for feature in categorical_features:  # Encode categorical features
        le = preprocessing.LabelEncoder()
        le.fit(train[feature])
        for table in tables:
            table[feature] = le.transform(table[feature])

    print("Getting features...")
    features = get_features(train, test)

    return train, test, features


def train_and_test_linear(train, test, features, target='price'):  # simple xgboost
    subsample = 0.8
    colsample_bytree = 0.8
    num_boost_round = 1200  # 115 originally
    early_stopping_rounds = 50
    test_size = 0.2  # 0.1 originally

    start_time = time.time()

    # start the training

    params = {
        "objective": "reg:linear",
        "booster": "gblinear",  # "gbtree",# default
        "eval_metric": "rmse",
        "subsample": subsample,  # collect 80% of the data only to prevent overfitting
        "colsample_bytree": colsample_bytree,
        "silent": 1,
        "seed": 0,
    }

    X_train, X_valid = train_test_split(train, test_size=test_size,
                                        random_state=0)  # randomly split into 90% test and 10% CV -> still has the outcome at this point
    y_train = np.log(X_train[target])  # define y as the outcome column, apply log to have same error as the leaderboard
    y_valid = np.log(X_valid[target])
    dtrain = xgb.DMatrix(X_train[features], y_train)  # DMatrix are matrix for xgboost
    dvalid = xgb.DMatrix(X_valid[features], y_valid)

    watchlist = [(dtrain, 'train'), (dvalid, 'eval')]  # list of things to evaluate and print
    gbm = xgb.train(params, dtrain, num_boost_round, evals=watchlist, early_stopping_rounds=early_stopping_rounds,
                    verbose_eval=True)  # find the best score
    score = gbm.best_score  # roc_auc_score(X_valid[target].values, check)
    print('Last error value: {:.6f}'.format(score))

    print("Predict test set...")
    test_prediction = gbm.predict(xgb.DMatrix(test[features]))

    print('Training time: {} minutes'.format(round((time.time() - start_time) / 60, 2)))

    return test_prediction, score


def train_and_test_tree(train, test, features, target='price'):  # simple xgboost
    eta_list = [0.1, 0.2]  # list of parameters to try
    max_depth_list = [4, 6, 8]  # list of parameters to try
    subsample = 0.8
    colsample_bytree = 0.8

    num_boost_round = 400
    early_stopping_rounds = 10
    test_size = 0.2

    start_time = time.time()

    # start the training
    array_score = np.ndarray((len(eta_list) * len(max_depth_list), 3))  # store score values
    i = 0
    for eta, max_depth in list(
            itertools.product(eta_list, max_depth_list)):  # Loop over parameters to find the better set
        print('XGBoost params. ETA: {}, MAX_DEPTH: {}, SUBSAMPLE: {}, COLSAMPLE_BY_TREE: {}'.format(eta, max_depth,
                                                                                                    subsample,
                                                                                                    colsample_bytree))
        params = {
            "objective": "reg:linear",
            "booster": "gbtree",
            "eval_metric": "rmse",  # this is the metric for the leardboard
            "eta": eta,  # shrinking parameters to prevent overfitting
            "tree_method": 'exact',
            "max_depth": max_depth,
            "subsample": subsample,  # collect 80% of the data only to prevent overfitting
            "colsample_bytree": colsample_bytree,
            "silent": 1,
            "seed": 0,
        }

        X_train, X_valid = train_test_split(train, test_size=test_size,
                                            random_state=0)  # randomly split into 90% test and 10% CV -> still has the outcome at this point
        y_train = np.log(X_train[target])  # define y as the outcome column
        y_valid = np.log(X_valid[target])
        dtrain = xgb.DMatrix(X_train[features], y_train)  # DMatrix are matrix for xgboost
        dvalid = xgb.DMatrix(X_valid[features], y_valid)

        watchlist = [(dtrain, 'train'), (dvalid, 'eval')]  # list of things to evaluate and print
        gbm = xgb.train(params, dtrain, num_boost_round, evals=watchlist, early_stopping_rounds=early_stopping_rounds,
                        verbose_eval=True)  # find the best score

        print("Validating...")
        score = gbm.best_score
        print('Last error value: {:.6f}'.format(score))
        array_score[i][0] = eta
        array_score[i][1] = max_depth
        array_score[i][2] = score
        i += 1
    df_score = pd.DataFrame(array_score, columns=['eta', 'max_depth', 'price'])
    print("df_score : \n", df_score)
    # create_feature_map(features)
    importance = gbm.get_fscore()
    importance = sorted(importance.items(), key=itemgetter(1), reverse=True)
    print('Importance array: ', importance)
    np.save("features_importance", importance)  # save feature importance for latter use
    print("Predict test set...")
    test_prediction = gbm.predict(xgb.DMatrix(test[features]),
                                  ntree_limit=gbm.best_ntree_limit)  # only predict with the last set of parameters

    print('Training time: {} minutes'.format(round((time.time() - start_time) / 60, 2)))

    return test_prediction, score


def train_and_test_Kfold(train, test, features, target='price'):  # add Kfold
    eta_list = [0.01]  # list of parameters to try
    max_depth_list = [6]
    subsample = 1  # No subsampling, as we already use Kfold latter and we don't have that much data
    colsample_bytree = 1

    num_boost_round = 5500  # for small eta, increase this one
    early_stopping_rounds = 500
    n_folds = 12
    start_time = time.time()

    # start the training
    array_score = np.ndarray((len(eta_list) * len(max_depth_list), 4))  # store score values
    i = 0
    for eta, max_depth in list(
            itertools.product(eta_list, max_depth_list)):  # Loop over parameters to find the better set
        print('XGBoost params. ETA: {}, MAX_DEPTH: {}'.format(eta, max_depth))
        params = {
            "objective": "reg:linear",
            "booster": "gbtree",
            "eval_metric": "rmse",
            "eta": eta,  # shrinking parameters to prevent overfitting
            "tree_method": 'exact',
            "max_depth": max_depth,
            "subsample": subsample,  # collect 80% of the data only to prevent overfitting
            "colsample_bytree": colsample_bytree,
            "silent": 1,
            "seed": 0,
        }
        kf = KFold(len(train), n_folds=n_folds)
        test_prediction = np.ndarray((n_folds, len(test)))
        fold = 0
        fold_score = []
        for train_index, cv_index in kf:
            X_train, X_valid = train[features].as_matrix()[train_index], train[features].as_matrix()[cv_index]
            y_train, y_valid = np.log(train[target].as_matrix()[train_index]), np.log(
                train[target].as_matrix()[cv_index])

            dtrain = xgb.DMatrix(X_train, y_train)  # DMatrix are matrix for xgboost
            dvalid = xgb.DMatrix(X_valid, y_valid)

            watchlist = [(dtrain, 'train'), (dvalid, 'eval')]  # list of things to evaluate and print
            gbm = xgb.train(params, dtrain, num_boost_round, evals=watchlist,
                            early_stopping_rounds=early_stopping_rounds, verbose_eval=True)  # find the best score

            print("Validating...")
            check = gbm.predict(xgb.DMatrix(X_valid))  # get the best score
            score = gbm.best_score
            print('Check last score value: {:.6f}'.format(score))
            fold_score.append(score)
            importance = gbm.get_fscore()
            importance = sorted(importance.items(), key=itemgetter(1), reverse=True)
            print('Importance array for fold {} :\n {}'.format(fold, importance))
            # np.save("features_importance",importance)
            print("Predict test set...")
            prediction = gbm.predict(xgb.DMatrix(test[features].as_matrix()))
            # np.save("prediction_eta%s_depth%s_fold%s" %(eta,max_depth,fold),prediction) # You can save all the folds prediction to check for errors in code
            test_prediction[fold] = prediction
            fold = fold + 1
        mean_score = np.mean(fold_score)
        print("Mean Score : {}, eta : {}, depth : {}\n".format(mean_score, eta, max_depth))
        array_score[i][0] = eta
        array_score[i][1] = max_depth
        array_score[i][2] = mean_score
        array_score[i][3] = np.std(fold_score)
        i += 1
    final_prediction = test_prediction.mean(axis=0)
    df_score = pd.DataFrame(array_score, columns=['eta', 'max_depth', 'mean_score', 'std_score'])
    print("df_score : \n", df_score)  # get the complete array of scores to choose the right parameters

    print('Training time: {} minutes'.format(round((time.time() - start_time) / 60, 2)))

    return final_prediction, mean_score


############################################################################
# Main code
###########################################################################

num_features = None  # Choose how many features you want to use. None = all

train = pd.read_csv('soldsold.csv')
test = pd.read_csv('azmarket.csv')

train = train.dropna(subset = ["price", "sqft", "bedrooms", "bathrooms"])
train = train.drop("county", 1)


test = test.dropna(subset = ["price", "sqft", "bedrooms", "bathrooms"])
test = test.drop("price", 1)
test = test.drop("county", 1)

train, test, features = process_features(train, test)

# test_prediction,score = train_and_test_linear(train,test,features)
# test_prediction,score = train_and_test_tree(train,test,features) # run at least once this one to get the features importance
# features=np.load("features_importance.npy")
test_prediction, score = train_and_test_Kfold(train, test, features[:num_features])

write_to_csv(np.exp(test_prediction), score)
