import pandas as pd
import time
import requests

CHURN_THRESHOLD = 0.7
POLL_INTERVAL = 60

# Function to check for new high-risk customers

def check_new_customers():
    print("Checking for new customer data...")

    df = pd.read_csv("customer_data.csv")
    new_customers = df[df['checked']  == 0]

    for index, row in new_customers.iterrows():
        if row  ['churn_probability'] > CHURN_THRESHOLD:

            features = []
            if row['low_engagement']: features.append("Low engagement")
            if row['high_complaints']: features.append("High complaint rate")
            if row['delayed_payments']: features.append("Delayed payments")

            features_text = ", ".join(features)
            # Call API for retention recommendations
            response = requests.post("http://127.0.0.1:5001/retention_strategy", json={"features": features_text})

            
            if response.status_code == 200:
                retention_strategy = response.json().get("retention_strategy", [])
                print(f"🚨 ALERT: High-risk customer {row['customer_id']}")
                print(f"   - Churn Probability: {row['churn_probability']:.2f}")
                print(f"   - Factors: {features_text}")
                print(f"   - Suggested Retention Strategy: {retention_strategy}\n")
            else:
                print(f"❌ Error calling API for customer {row['customer_id']}")

            # Mark customer as checked
            df.at[index, 'checked'] = 1

    # Save updated database
    df.to_csv("customer_data.csv", index=False)

# Run polling loop
while True:
    check_new_customers()
    time.sleep(POLL_INTERVAL)    