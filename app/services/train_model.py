import pandas as pd
from xgboost import XGBClassifier
import joblib
from sklearn.model_selection import train_test_split

# 1. Load Data (Download 'PS_20174392719_1491204439457_log.csv' from Kaggle)
df = pd.read_csv('PS_20174392719_1491204439457_log.csv')

# 2. Preprocessing (Hackathon Speed Version)
# Fraud usually happens in TRANSFER and CASH_OUT
df = df[df['type'].isin(['TRANSFER', 'CASH_OUT'])]

# Create features that catch 'Emptying the account'
df['errorBalanceSender'] = df['amount'] + df['newbalanceOrig'] - df['oldbalanceOrg']
df['errorBalanceReceiver'] = df['oldbalanceDest'] + df['amount'] - df['newbalanceDest']

X = df[['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest', 'errorBalanceSender', 'errorBalanceReceiver']]
y = df['isFraud']

# 3. Train the Beast
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = XGBClassifier(n_estimators=100, max_depth=5)
model.fit(X_train, y_train)

# 4. Save it for the FastAPI
joblib.dump(model, 'app/models/fraud_model.pkl')
print("Model Brain Created!")