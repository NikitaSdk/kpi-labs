import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report
from sklearn.preprocessing import StandardScaler

train = pd.read_csv("application_train.csv")
test = pd.read_csv("application_test.csv")
train.shape, test.shape



test.head()
train.head()

train.replace('XNA', np.nan, inplace=True)
test.replace('XNA', np.nan, inplace=True)
data_missing = pd.concat([
    ((train.isnull().sum() / len(train)) * 100),
    ((test.isnull().sum() / len(test)) * 100)
], axis=1)

data_missing.columns = ['Train', 'Test']
missing_columns = data_missing[data_missing.any(axis=1)]
if not missing_columns.empty:
    print(missing_columns.to_string())




categorical_columns = train.select_dtypes(include=['object', 'category']).columns.tolist()

keyword_columns = train.filter(like='FLAG').columns.tolist()
keyword_columns += ['REG_REGION_NOT_LIVE_REGION',
                    'REG_REGION_NOT_WORK_REGION',
                    'LIVE_REGION_NOT_WORK_REGION',
                    'REG_CITY_NOT_LIVE_CITY',
                    'REG_CITY_NOT_WORK_CITY',
                    'LIVE_CITY_NOT_WORK_CITY']

categorical_columns += keyword_columns

for column in categorical_columns:
    train[column] = train[column].astype("category")
    test[column] = test[column].astype("category")
    unique_values = train[column].unique()
    print(column, unique_values)
    print()


if 'WEEKDAY_APPR_PROCESS_START' in categorical_columns:
    categorical_columns.remove('WEEKDAY_APPR_PROCESS_START')


numeric_columns = train.select_dtypes(exclude=['object', 'category']).columns.tolist()

numeric_columns_to_categorical = [col for col in numeric_columns if train[col].nunique() <= 3 and col != 'TARGET']

categorical_columns.extend(numeric_columns_to_categorical)

numeric_columns = [col for col in numeric_columns if col not in numeric_columns_to_categorical]

if 'SK_ID_CURR' in numeric_columns:
    numeric_columns.remove('SK_ID_CURR')

print("Numeric columns:", numeric_columns)




sns.heatmap(train[numeric_columns].corr(), cmap='RdYlBu')


train[numeric_columns].hist(figsize=(16, 20))

ncols = 5
nrows = len(categorical_columns) // ncols
if len(categorical_columns) % ncols != 0:
    nrows += 1
fig, axs = plt.subplots(nrows, ncols, figsize=(ncols*5, nrows*4))
for col, ax in zip(categorical_columns, axs.ravel()):
    sns.histplot(train[col], kde=False, ax=ax, color='pink', label='Original')
    sns.histplot(test[col], kde=False, ax=ax, color='yellow', label='Test')
    ax.set_title(f'Distribution of {col}')
    ax.legend()

plt.tight_layout()
plt.show()


ncols = 5
nrows = len(numeric_columns) // ncols
if len(numeric_columns) % ncols != 0:
    nrows += 1
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 5, nrows * 4))
for i, col in enumerate(numeric_columns):
    sns.boxplot(train[col], ax=axes[i // ncols, i % ncols])
    axes[i // ncols, i % ncols].set_xlabel(col)
plt.tight_layout()
plt.show()



target_counts = train['TARGET'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(target_counts, labels=target_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of TARGET')
plt.show()


def fill_missing_values(data):
    numeric_columns = data.select_dtypes(include=['int', 'float']).columns
    categorical_columns = data.select_dtypes(include=['object', 'category']).columns

    for col in numeric_columns:
        mean_value = data[col].mean()
        data[col].fillna(mean_value, inplace=True)
        print(f'Filled missing values for {col} with mean: {mean_value}')

    for col in categorical_columns:
        mode_value = data[col].mode()[0]
        data[col].fillna(mode_value, inplace=True)
        print(f'Filled missing values for {col} with mode: {mode_value}')

    return data


def preprocess_data(train, test):
    print("Filling missing values...")
    train = fill_missing_values(train)
    test = fill_missing_values(test)



    train.drop_duplicates(inplace=True)
    test.drop_duplicates(inplace=True)
    print("Duplicates removed.")

    numeric_columns_train = train.select_dtypes(exclude=['object', 'category']).columns.tolist()
    numeric_columns_test = test.select_dtypes(exclude=['object', 'category']).columns.tolist()
    numeric_columns_train.remove('TARGET')
    numeric_columns_train.remove('SK_ID_CURR')
    numeric_columns_test.remove('SK_ID_CURR')
    train[numeric_columns_train] = StandardScaler().fit_transform(train[numeric_columns_train])
    test[numeric_columns_test] = StandardScaler().fit_transform(test[numeric_columns_test])
    print("Numeric columns scaled.")

    train = pd.get_dummies(train, columns=train.select_dtypes(include=['category']).columns, drop_first=True, dtype=int)
    test = pd.get_dummies(test, columns=test.select_dtypes(include=['category']).columns, drop_first=True, dtype=int)
    print("Categorical columns encoded.")

    return train, test

processed_train, processed_test = preprocess_data(train, test)


processed_train = processed_train.drop(['SK_ID_CURR'], axis=1)


X_train, X_val, y_train, y_val = train_test_split(processed_train.drop(['TARGET'], axis=1), processed_train['TARGET'], test_size=0.15, random_state=42)

missing_columns = set(X_train.columns) - set(processed_test.columns)
X_train = X_train.drop(columns=missing_columns)
X_val = X_val.drop(columns=missing_columns)

print("Shapes after splitting and dropping missing columns:")
print("X_train shape:", X_train.shape)
print("X_val shape:", X_val.shape)
print("y_train shape:", y_train.shape)
print("y_val shape:", y_val.shape)
print("processed_test shape:", processed_test.shape)

processed_test.shape

model = LogisticRegression(class_weight='balanced', random_state=42, solver='saga', penalty='elasticnet', C=1, l1_ratio=0.5, n_jobs=-1, max_iter=500)

model.fit(X_train, y_train)




y_pred = model.predict(X_val)
report = classification_report(y_val, y_pred)
print("Classification Report:")
print(report)

y_pred_proba = model.predict_proba(X_val)[:, 1]
roc_auc = roc_auc_score(y_val, y_pred_proba)
print("ROC AUC Score:", roc_auc)

y_test_pred_proba = model.predict_proba(processed_test.drop(['SK_ID_CURR'], axis=1))[:, 1]
submission = pd.DataFrame({'SK_ID_CURR': processed_test['SK_ID_CURR'], 'TARGET': y_test_pred_proba})
submission.to_csv('submission.csv', index=False)
print(submission)
