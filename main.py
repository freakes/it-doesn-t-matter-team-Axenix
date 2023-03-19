import numpy
import pandas as pd
import random as r
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import numpy as np
import psycopg2
import datetime

pd.set_option('display.max_rows', 5000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

with open('employers.txt', 'r') as emp:
    EMPLOYERS = emp.read().split(';')
    emp.close()
RECENT_DATE = str(datetime.datetime.now()).split()[0].split('-')[-1]


def time_check_messages(name):
    cur_emp = data_messages.loc[data_messages['employer'] == name]
    counter = 0
    week = []
    for i in range(len(cur_emp)):
        if len(week) != 10:
            week.append(cur_emp.iloc[i]['num_message'])
        else:
            if (min(week) + (sum(week) / len(week)) * 0.5) < sum(week) / len(week):
                counter += 1
                print(week)
            week = []
    return counter


def time_check_commits(name):
    cur_emp = data_commits.loc[data_commits['employer'] == name]
    counter = 0
    week = []
    for i in range(len(cur_emp)):
        if len(week) != 10:
            week.append(cur_emp.iloc[i]['text'])
        else:
            for el in week:
                if ('fix' in el.lower() and len(el) < 11) or \
                        len(el) < 11:
                    counter += 1
            if counter >= 5:
                return 5
            week = []
    return 0


def time_check_task_manager(name):
    cur_emp = data_task_manager.loc[data_task_manager['employer'] == name]
    counter = 0
    week = []
    for i in range(len(cur_emp)):
        if len(week) != 10:
            week.append(cur_emp.iloc[i]['bad_relocating'])
        else:
            if 5.0 in week or 5 in week:
                counter += 1
            week = []
    return counter


def time_check_apps(name):
    cur_emp = data_apps.loc[data_apps['employer'] == name]
    counter = 0
    week = []
    for i in range(len(cur_emp)):
        if len(week) != 10:
            week.append(cur_emp.iloc[i]['time_work'])
        else:
            for el in week:
                if el <= 5:
                    counter += 1
            week = []
    return counter


# TODO apps
def get_apps(data_apps, to_predict=False):

    data_apps = data_apps.sort_values(by='timestamp',
                                      key=lambda s: s.apply(lambda x: [int(x.split('-')[1]), int(x.split('-')[0])]))
    data_apps = data_apps.drop(columns=['chill_app', 'work_app', 'Unnamed: 0', 'timestamp'])
    new_df = data_apps.copy()

    data_apps_gr = data_apps.groupby('employer').mean()
    new_df_gr = new_df.groupby('employer').mean()

    if to_predict:
        X = data_apps_gr.iloc[:, :-1].values
        y = data_apps_gr.iloc[:, -1].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        regressor = RandomForestRegressor()
        regressor.fit(X_train, y_train)
        res = []
        for el in EMPLOYERS:
            y_pred = regressor.predict([numpy.array([new_df_gr.loc[[el], 'time_chill'][0], new_df_gr.loc[[el], 'time_work'][0]])])
            res.append(y_pred[0])

        return res
    return data_apps_gr


# TODO commits
def get_commits(data_commits, to_predict=False):

    data_commits = data_commits.drop(columns=['Unnamed: 0', 'text'])
    new_df = data_commits.copy()
    data_commits = data_commits.sort_values(by='timestamp', key=lambda s: s.apply(lambda x: [x]))
    new_df = new_df.sort_values(by='timestamp', key=lambda s: s.apply(lambda x: [x]))
    for el in EMPLOYERS:
        new_df.loc[[el], 'timestamp'] = new_df.loc[[el], 'timestamp'].iloc[0] + 100

    data_commits_gr = data_commits.groupby('employer').mean()
    new_df_gr = new_df.groupby('employer').mean()
    if to_predict:
        X = data_commits_gr.iloc[:, :-1].values
        y = data_commits_gr.iloc[:, -1].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        regressor = RandomForestRegressor()
        regressor.fit(X_train, y_train)

        res = []
        for el in EMPLOYERS:
            y_pred = regressor.predict([numpy.array([new_df_gr.loc[[el], 'timestamp'][0], new_df_gr.loc[[el], 'commit_len'][0]])])
            res.append(y_pred[0])

        return res
    return data_commits_gr


# TODO messages
def get_messages(data_messages, to_predict=False):
    data_messages = data_messages.sort_values(by='timestamp', key=lambda s: s.apply(
        lambda x: [int(x.split('-')[1]), int(x.split('-')[0])]))
    data_messages = data_messages.drop(columns=['Unnamed: 0'])
    new_df = data_messages.copy()
    for el in EMPLOYERS:
        data_messages.loc[[el], 'timestamp'] = int(
            ''.join(data_messages.loc[[el], 'timestamp'].iloc[0].split('-')[::-1]))

    for el in EMPLOYERS:
        new_df.loc[[el], 'timestamp'] = (int(
            ''.join(new_df.loc[[el], 'timestamp'].iloc[0].split('-')[::-1])) + 100)

    data_messages_gr = data_messages.groupby('employer').mean()
    new_df_gr = new_df.groupby('employer').mean()

    if to_predict:
        X = data_messages_gr.iloc[:, :-1].values
        y = data_messages_gr.iloc[:, -1].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        regressor = RandomForestRegressor()
        regressor.fit(X_train, y_train)

        res = []
        for el in EMPLOYERS:
            y_pred = regressor.predict([new_df_gr.loc[[el], 'num_message']])
            res.append(y_pred[0])

        return res
    return data_messages_gr


# TODO task_manager
def get_task_manager(data_task_manager, to_predict=False):

    data_task_manager = data_task_manager.sort_values(by='timestamp', key=lambda s: s.apply(
        lambda x: [int(x.split('-')[1]), int(x.split('-')[0])]))
    data_task_manager = data_task_manager.drop(columns=['Unnamed: 0'])
    new_df = data_task_manager.copy()
    for el in EMPLOYERS:
        data_task_manager.loc[[el], 'timestamp'] = int(
            ''.join(data_task_manager.loc[[el], 'timestamp'].iloc[0].split('-')[::-1]))

    for el in EMPLOYERS:
        new_df.loc[[el], 'timestamp'] = (int(
            ''.join(new_df.loc[[el], 'timestamp'].iloc[0].split('-')[::-1])) + 100)

    data_task_manager_gr = data_task_manager.groupby('employer').mean()
    new_df_gr = new_df.groupby('employer').mean()
    if to_predict:

        X = data_task_manager_gr.iloc[:, :-1].values
        y = data_task_manager_gr.iloc[:, -1].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        regressor = RandomForestRegressor()
        regressor.fit(X_train, y_train)
        res = []
        for el in EMPLOYERS:
            y_pred = regressor.predict([new_df_gr.loc[[el], 'bad_relocating']])
            res.append(y_pred[0])
        y_pred_new = regressor.predict(X_test)

        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred_new))
        print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred_new))
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred_new)))

        return res
    return data_task_manager_gr


def fill_coeffs_task_manager():
    res = []
    data_task_manager = pd.read_csv('task_manager.csv', index_col=0)
    for el in EMPLOYERS:
        res.append(time_check_task_manager(el))
    sorted(res, reverse=True)

    for i in range(len(data_task_manager)):
        coef = time_check_apps(data_task_manager.iloc[i]['employer'])
        if coef > 0:
            data_task_manager.loc[[i], 'coef'] = coef * 0.5
        else:
            data_task_manager.loc[[i], 'coef'] = 0
    data_task_manager.to_csv('task_manager.csv')


def fill_coeffs_apps():
    data_apps = pd.read_csv('apps.csv', index_col=0)

    for i in range(len(data_task_manager)):
        coef = time_check_apps(data_apps.iloc[i]['employer'])
        if coef > 0:
            data_apps.loc[[i], 'coef'] = coef * 0.5
        else:
            data_apps.loc[[i], 'coef'] = 0
    data_apps.to_csv('apps (2).csv')


def fill_coeffs_messages():
    res = []
    data_messages = pd.read_csv('messages.csv', index_col=0)
    for el in EMPLOYERS:
        res.append(time_check_messages(el))
    sorted(res, reverse=True)
    mid = sum(res) / len(res)

    for i in range(len(data_messages)):
        coef = time_check_apps(data_messages.iloc[i]['employer'])
        if coef > 0:
            data_messages.loc[[i], 'coef'] = mid - coef
        else:
            data_messages.loc[[i], 'coef'] = 0
    data_messages.to_csv('messages.csv')


def fill_coeffs_commits():
    data_commits = pd.read_csv('commits.csv', index_col=0)

    for i in range(len(data_commits)):
        coef = time_check_commits(data_commits.iloc[i]['employer'])
        if coef > 0:
            data_commits.loc[[i], 'coef'] = coef
        else:
            data_commits.loc[[i], 'coef'] = 0
    data_commits.to_csv('commits1.csv')


CONN = psycopg2.connect(dbname='Axenix', user='postgres', password='Polina', host='localhost')
CURSOR = CONN.cursor()


def get_all_data():
    if str(datetime.datetime.now()).split()[0].split('-')[-1] != RECENT_DATE:
        fetch_data()
    CURSOR.execute("SELECT * FROM data_coefs")
    records = CURSOR.fetchall()
    return records


def fetch_data():
    fill_coeffs_task_manager()
    fill_coeffs_commits()
    fill_coeffs_messages()
    fill_coeffs_apps()
    data_task_manager = pd.read_csv('task_manager (2).csv', index_col=1)
    data_apps = pd.read_csv('apps.csv', index_col=1)
    data_commits = pd.read_csv('commits1.csv', index_col=1)
    data_messages = pd.read_csv('messages.csv', index_col=1)

    res = get_task_manager(data_task_manager) + get_apps(data_apps) + get_commits(data_commits) + get_messages(
        data_messages)
    res_pred = [a + b + c + d for a, b, c, d in
                zip(get_task_manager(data_task_manager, True), get_apps(data_apps, True),
                    get_commits(data_commits, True), get_messages(data_messages, True))]

    res = res.drop(columns=['bad_relocating', 'commit_len', 'num_message', 'time_chill', 'time_work', 'timestamp'])
    print(res)
    res_pred = pd.DataFrame({'future_coef': res_pred}, index=EMPLOYERS)
    print(res_pred)
    CURSOR.execute(f"DELETE FROM data_coefs")
    CONN.commit()
    for el in EMPLOYERS:
        CURSOR.execute(
            f"INSERT INTO data_coefs (employer, current_coef, future_coef) VALUES('{el}', {res.loc[[el], 'coef'][0]}, {res_pred.loc[[el], 'future_coef'][0]})")
    CONN.commit()
    CONN.close()


def check_user(login, password):
    CURSOR.execute(f"SELECT EXISTS (SELECT * FROM user_role WHERE user_login = '{login}' AND user_password = '{password}')")
    rec = CURSOR.fetchone()[0]
    return rec
