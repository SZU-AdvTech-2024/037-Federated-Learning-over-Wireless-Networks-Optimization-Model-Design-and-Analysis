import numpy as np
import csv
from keras.utils.np_utils import to_categorical
np.random.seed(0)


def get_iris_classification_non_iid_data(path, num_users, each_user_class_num):
    dict_users = {}
    features, labels = [], []
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile)
        for item in reader:
            features.append(item[0:-1])
            labels.append(item[-1])
    categorical_labels = to_categorical(labels, num_classes=3)
    for u in range(num_users):
        user_classes = np.random.choice([0, 1, 2], each_user_class_num, replace=False)
        user_idx = []
        for i, label in enumerate(labels):
            label = int(label)
            if label in user_classes:
                user_idx.append(i)
        dict_users[u] = set(user_idx)
    return features, categorical_labels, dict_users


def linear_non_iid_data_generation(path, size, length, num_users):
    each_user_data_num = length // num_users
    dict_users = {}
    all_features = []
    all_labels = []
    for u in range(num_users):
        features = np.random.rand(each_user_data_num, size) * (u + 1)
        w = np.random.rand(size)
        noise = (u + 1) / 10 * np.random.rand(each_user_data_num)
        b = np.random.rand(1)
        labels = np.add(np.add(np.dot(features, np.transpose(w)), b), np.transpose(noise))
        all_features.append(features)
        all_labels.append(labels)
    all_features = np.concatenate(np.array(all_features), axis=0)
    all_labels = np.concatenate(np.array(all_labels), axis=0)
    with open(path, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(np.hstack((all_features, all_labels.reshape(length, 1))))
    for u in range(num_users):
        dict_users[u] = set(range(u * each_user_data_num, u * each_user_data_num + each_user_data_num))
    return all_features, all_labels, dict_users


def linear_iid_data_generation(path, size, length):
    features = np.random.rand(length, size)
    w = np.random.rand(size)
    b = np.random.rand(1)
    noise = 0.1 * np.random.rand(length)
    labels = np.add(np.add(np.dot(features, np.transpose(w)), b), np.transpose(noise))
    with open(path, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(np.hstack((features, labels.reshape(length, 1))))
    return features, labels


def linear_iid(data_len, num_users):
    num_items = int(data_len/num_users)
    dict_users, all_idxs = {}, [i for i in range(data_len)]
    for i in range(num_users):
        dict_users[i] = set(np.random.choice(all_idxs, num_items, replace=False))
        all_idxs = list(set(all_idxs) - dict_users[i])
    return dict_users


def collect_data(data, idx):
    user_data = []
    for i in idx:
        user_data.append(data[i])
    return user_data
