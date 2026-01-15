
# 1️⃣ First: Feature Engineering Philosophy (Fraud Context)

Fraud is **behavioral + temporal + relational**.

Raw columns alone are weak.
Fraud signals emerge when we ask:

* ❓ *Is this transaction unusual for this customer/device/merchant?*
* ❓ *Is the timing suspicious?*
* ❓ *Is the network behavior abnormal?*
* ❓ *Is the amount inconsistent with history?*

So we engineer features in **5 layers**:

1. Time-based
2. Amount-based
3. Velocity / Frequency-based
4. Entity behavior (Customer / Device / Merchant)
5. Risk aggregation & encoding

---

# 2️⃣ Time-Based Feature Engineering (VERY IMPORTANT)

### Existing

* `Date`
* `Time`

### Create 👇

### 🔹 `transaction_hour`

```text
Hour extracted from Time (0–23)
```

**Why**

* Fraud spikes at **odd hours** (midnight–early morning)
* Humans sleep; bots don’t

---

### 🔹 `transaction_day`

```text
Day of month (1–31)
```

**Why**

* End-of-month / salary days → higher fraud attempts

---

### 🔹 `transaction_weekday`

```text
0=Monday … 6=Sunday
```

**Why**

* Weekend fraud patterns differ from weekdays

---

### 🔹 `is_weekend`

```text
1 if Saturday/Sunday else 0
```

**Why**

* Fraudsters exploit low-monitoring windows

---

### 🔹 `is_night_transaction`

```text
1 if hour ∈ [0–5] else 0
```

**Why**

* High-signal binary fraud indicator

---

# 3️⃣ Amount-Based Feature Engineering

### Existing

* `amount`
* `Transaction_Amount_Deviation` (already useful)

### Create 👇

### 🔹 `log_amount`

```text
log(amount + 1)
```

**Why**

* Amounts are heavy-tailed
* Helps ANN, Logistic, XGBoost converge better

---

### 🔹 `amount_bucket`

```text
low / medium / high / very_high (quantiles)
```

**Why**

* Fraud risk changes non-linearly with amount

---

### 🔹 `is_high_amount`

```text
1 if amount > 95th percentile
```

**Why**

* Captures rare but high-impact fraud

---

### 🔹 `amount_vs_deviation_ratio`

```text
amount / (Transaction_Amount_Deviation + ε)
```

**Why**

* Measures how abnormal the amount really is

---

# 4️⃣ Velocity & Frequency Features (CORE FRAUD SIGNALS)

### Existing

* `Transaction_Frequency`
* `Days_Since_Last_Transaction`

### Create 👇

### 🔹 `inverse_days_since_last_txn`

```text
1 / (Days_Since_Last_Transaction + 1)
```

**Why**

* Recent bursts = fraud
* Linear models prefer this form

---

### 🔹 `is_burst_transaction`

```text
1 if Days_Since_Last_Transaction <= 1
```

**Why**

* Fraud often happens in rapid bursts

---

### 🔹 `frequency_bucket`

```text
low / medium / high
```

**Why**

* Converts noisy numeric frequency into stable signal

---

# 5️⃣ Customer-Level Behavioral Features

Group by `Customer_ID`

### 🔹 `customer_avg_amount`

```text
Mean transaction amount per customer
```

**Why**

* Detect deviation from personal norm

---

### 🔹 `customer_std_amount`

```text
Std dev of customer amount
```

**Why**

* Fraud = spike relative to variance

---

### 🔹 `amount_vs_customer_avg`

```text
amount / customer_avg_amount
```

**Why**

* One of the strongest fraud indicators

---

### 🔹 `customer_txn_count`

```text
Total historical transactions
```

**Why**

* New customers are riskier

---

### 🔹 `is_new_customer`

```text
1 if customer_txn_count < threshold
```

**Why**

* Cold-start fraud risk

---

# 6️⃣ Device-Level Risk Features

Group by `Device_ID`

### 🔹 `device_txn_count`

```text
Number of transactions from same device
```

**Why**

* Fraud devices are reused

---

### 🔹 `unique_customers_per_device`

```text
Count distinct customers per device
```

**Why**

* One device → many customers = fraud ring

---

### 🔹 `device_fraud_rate`

```text
Past fraud % for that device
```

**Why**

* Extremely powerful for ensemble models

---

# 7️⃣ Merchant-Level Risk Features

Group by `Merchant_ID`

### 🔹 `merchant_fraud_rate`

```text
Historical fraud ratio
```

**Why**

* Some merchants are high-risk

---

### 🔹 `merchant_avg_amount`

```text
Mean amount per merchant
```

**Why**

* Contextualizes amount anomalies

---

### 🔹 `is_new_merchant`

```text
1 if merchant_txn_count < threshold
```

**Why**

* Fake or newly compromised merchants

---

# 8️⃣ Geo & Channel Risk Features

### Existing

* `Transaction_City`
* `Transaction_State`
* `Transaction_Channel`
* `IP_Address`

### Create 👇

### 🔹 `state_fraud_rate`

```text
Fraud % per state
```

**Why**

* Geo-risk modeling

---

### 🔹 `channel_risk_score`

```text
Encoded risk per channel (Online > POS)
```

**Why**

* Online channels are riskier

---

### 🔹 `ip_device_match`

```text
1 if IP seen with this device before
```

**Why**

* IP hopping is a fraud signal

---

# 9️⃣ Encoding Strategy (IMPORTANT)

| Feature Type               | Encoding                |
| -------------------------- | ----------------------- |
| High-cardinality IDs       | Target encoding         |
| Low-cardinality categories | One-hot                 |
| ANN input                  | Normalized + embeddings |
| Autoencoder                | Numeric only            |

---

# 🔟 Why This Feature Set Is Industry-Grade

✔ Works for **Logistic, XGBoost, RandomForest**
✔ Works for **ANN & Autoencoders**
✔ Supports **data drift detection**
✔ Supports **model drift monitoring**
✔ Reproducible via **DVC**
✔ Trackable via **MLflow**

---

# Next Steps (Tell Me When Ready)

👉 **Next response** I will:

1. Design **feature engineering pipeline (train vs inference safe)**
2. Show **leakage-free aggregation**
3. Decide **which features for which model**
4. Prepare **DVC structure**
5. Prepare **MLflow experiment plan**

When you’re ready, say **“Next: feature pipeline design”** 🚀
