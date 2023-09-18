import pandas as pd
import datetime as dt
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline
sns.set_theme()
sns.set_palette('colorblind')
traffic = pd.read_csv('traffic.csv')
smartphones = pd.read_csv('crashes_smartphones.csv')

print(traffic.dtypes)
traffic['Date'] = pd.to_datetime(traffic['Date'])
print(traffic.dtypes)

sns.lineplot(data=traffic, x='Date', y='Crashes_per_100k')
plt.title('Traffic Safety: Crashes per 100,000 People over Time')
plt.xlabel('Date')
plt.ylabel('Crashes per 100,000 People')
plt.show()

sns.boxplot(data=traffic[traffic.Date.dt.year != 2020], x='Season', y='Crashes_per_100k')
plt.title('Traffic Safety: Crash Rate Variation by Season')
plt.xlabel('Season')
plt.ylabel('Crashes per 100,000 People')
plt.show()

print(smartphones.head())

smartphones['Smartphone_Survey_Date'] = pd.to_datetime(smartphones['Smartphone_Survey_Date'])
print(smartphones.dtypes)

sns.lineplot(data=smartphones, x='Smartphone_Survey_Date', y='Smartphone_usage')
plt.title('Smartphone Usage Over Time')
plt.xlabel('Survey Date')
plt.ylabel('Smartphone Usage (%)')
plt.show()

sns.regplot(data=smartphones, x='Smartphone_usage', y='Crashes_per_100k')
plt.title('Crash Rate by Smartphone Usage')
plt.xlabel('Smartphone Usage (%)')
plt.ylabel('Crashes per 100,000 People')
plt.show()

corr, p = pearsonr(smartphones['Smartphone_usage'], smartphones['Crashes_per_100k'])
print('Correlation coefficient:', corr)
print('p-value:', p)

X = smartphones['Smartphone_usage'].values.reshape(-1, 1)
y = smartphones['Crashes_per_100k'].values
lm = LinearRegression()
lm.fit(X, y)

print('Intercept:', lm.intercept_)
print('Coefficient:', lm.coef_)

usage_2019 = smartphones.loc[smartphones['Smartphone_Survey_Date'] == '2019-01-01', 'Smartphone_usage'].values[0]

crash_rate_2020_predicted = lm.predict([[usage_2019]])[0]
print('Predicted crash rate for 2020:', crash_rate_2020_predicted)

actual_crash_rate_2020 = traffic.loc[traffic['Date'] == '2020-02-01', 'Crashes_per_100k'].values[0]
print('Actual crash rate for February 2020:', actual_crash_rate_2020)

sns.regplot(data=smartphones

fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# Gráfico 1:
sns.regplot(data=smartphones, x='Smartphone_usage', y='Crashes_per_100k', ax=ax[0])
ax[0].set_title('Crash Rate by Smartphone Usage')
ax[0].set_xlabel('Smartphone Usage (%)')
ax[0].set_ylabel('Crashes per 100,000 People')

# Gráfico 2:
sns.regplot(data=smartphones, x='Smartphone_usage', y='Crashes_per_100k', ax=ax[1])
ax[1].scatter(usage_2019, crash_rate_2020_predicted, color='red', marker='o', label='Predicted Crash Rate 2020')
ax[1].scatter(usage_2019, actual_crash_rate_2020, color='green', marker='o', label='Actual Crash Rate Feb 2020')
ax[1].set_title('Comparison of Predicted and Actual Crash Rates')
ax[1].set_xlabel('Smartphone Usage (%)')
ax[1].set_ylabel('Crashes per 100,000 People')
ax[1].legend()

plt.tight_layout()
plt.show()
