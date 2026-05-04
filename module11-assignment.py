# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

np.random.seed(42)

quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(loc=100000, scale=20000)

            seasonal_factor = 1.0
            if quarter.quarter == 4:
                seasonal_factor = 1.3
            elif quarter.quarter == 1:
                seasonal_factor = 0.8

            location_factor = {'Tampa':1.0,'Miami':1.2,'Orlando':0.9,'Jacksonville':0.8}[location]
            category_factor = {'Electronics':1.5,'Clothing':1.0,'Home Goods':0.8,'Sporting Goods':0.7,'Beauty':0.9}[category]

            growth_factor = (1 + 0.05/4) ** quarter_idx

            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)

            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)

            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

customer_data = []
total_customers = 2000

age_params = {
    'Tampa': (45, 15),
    'Miami': (35, 12),
    'Orlando': (38, 14),
    'Jacksonville': (42, 13)
}

for location in locations:
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {'Tampa':0.3,'Miami':0.35,'Orlando':0.2,'Jacksonville':0.15}[location])

    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)

    for age in ages:
        base_amount = np.random.gamma(shape=5, scale=20)
        price_tier = np.random.choice(['Budget','Mid-range','Premium'], p=[0.3,0.5,0.2])
        tier_factor = {'Budget':0.7,'Mid-range':1.0,'Premium':1.8}[price_tier]
        purchase_amount = base_amount * tier_factor

        customer_data.append({
            'Location': location,
            'Age': age,
            'PurchaseAmount': round(purchase_amount,2),
            'PriceTier': price_tier
        })

sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']


# ---------------- VISUALS ---------------- #

def plot_quarterly_sales_trend():
    df = sales_df.groupby('QuarterLabel')['Sales'].sum()
    fig, ax = plt.subplots()
    ax.plot(df.index, df.values, marker='o')
    ax.set_title("Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    ax.grid()
    return fig


def plot_location_sales_comparison():
    df = sales_df.groupby(['QuarterLabel','Location'])['Sales'].sum().unstack()
    fig, ax = plt.subplots()
    for col in df.columns:
        ax.plot(df.index, df[col], marker='o', label=col)
    ax.legend()
    ax.set_title("Sales by Location")
    return fig


def plot_category_performance_by_location():
    latest = sales_df[sales_df['QuarterLabel']=="Q4 2023"]
    df = latest.groupby(['Location','Category'])['Sales'].sum().unstack()
    fig, ax = plt.subplots()
    df.plot(kind='bar', ax=ax)
    ax.set_title("Category Performance by Location")
    return fig


def plot_sales_composition_by_location():
    df = sales_df.groupby(['Location','Category'])['Sales'].sum().unstack()
    df = df.div(df.sum(axis=1), axis=0)
    fig, ax = plt.subplots()
    df.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Sales Composition by Location")
    return fig


def plot_ad_spend_vs_sales():
    fig, ax = plt.subplots()
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'])
    ax.set_title("Ad Spend vs Sales")
    ax.set_xlabel("Ad Spend")
    ax.set_ylabel("Sales")
    return fig


def plot_ad_efficiency_over_time():
    df = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()
    fig, ax = plt.subplots()
    ax.plot(df.index, df.values, marker='o')
    ax.set_title("Ad Efficiency Over Time")
    return fig


def plot_customer_age_distribution():
    fig, axs = plt.subplots(2,2)
    axs = axs.flatten()

    for i, loc in enumerate(customer_df['Location'].unique()):
        data = customer_df[customer_df['Location']==loc]['Age']
        axs[i].hist(data)
        axs[i].set_title(loc)

    return fig


def plot_purchase_by_age_group():
    bins = [18,30,45,60,80]
    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins)
    fig, ax = plt.subplots()
    customer_df.boxplot(column='PurchaseAmount', by='AgeGroup', ax=ax)
    return fig


def plot_purchase_amount_distribution():
    fig, ax = plt.subplots()
    ax.hist(customer_df['PurchaseAmount'])
    return fig


def plot_sales_by_price_tier():
    df = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    fig, ax = plt.subplots()
    ax.pie(df.values, labels=df.index, autopct='%1.1f%%')
    return fig


def plot_category_market_share():
    df = sales_df.groupby('Category')['Sales'].sum()
    fig, ax = plt.subplots()
    ax.pie(df.values, labels=df.index, autopct='%1.1f%%')
    return fig


def plot_location_sales_distribution():
    df = sales_df.groupby('Location')['Sales'].sum()
    fig, ax = plt.subplots()
    ax.pie(df.values, labels=df.index, autopct='%1.1f%%')
    return fig


def create_business_dashboard():
    fig, axs = plt.subplots(2,2)

    sales_df.groupby('QuarterLabel')['Sales'].sum().plot(ax=axs[0,0], title="Sales Trend")
    sales_df.groupby('Location')['Sales'].sum().plot(kind='bar', ax=axs[0,1], title="Sales by Location")
    customer_df['PurchaseAmount'].hist(ax=axs[1,0])
    sales_df.groupby('Category')['Sales'].sum().plot(kind='pie', ax=axs[1,1])

    return fig


def main():
    plot_quarterly_sales_trend()
    plot_location_sales_comparison()
    plot_category_performance_by_location()
    plot_sales_composition_by_location()
    plot_ad_spend_vs_sales()
    plot_ad_efficiency_over_time()
    plot_customer_age_distribution()
    plot_purchase_by_age_group()
    plot_purchase_amount_distribution()
    plot_sales_by_price_tier()
    plot_category_market_share()
    plot_location_sales_distribution()
    create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("1. Sales increase over time with strong Q4 spikes.")
    print("2. Miami consistently generates the highest revenue.")
    print("3. Electronics is the top-performing category.")
    print("4. Advertising positively correlates with sales.")
    print("5. Mid-range products dominate purchases.")
    print("6. Customer age varies by location, with Miami being younger.")

    plt.show()


if __name__ == "__main__":
    main()