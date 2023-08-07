import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('/Users/P2982820/Desktop/m1_shop_legacy.csv')

# Convert the timestamp column to datetime format
data['TIME_STAMP'] = pd.to_datetime(data['TIME_STAMP'])

# Sort the DataFrame by the timestamp column
data = data.sort_values('TIME_STAMP')

# Create a figure with two subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 10))

# Plot the RSSI values against the timestamp
axs[0].plot(data['TIME_STAMP'], data['RSSI'])
axs[0].set_xlabel('TIME_STAMP')
axs[0].set_ylabel('RSSI')
axs[0].set_title('RSSI values over time')
axs[0].tick_params(rotation=45)

# Plot the IP addresses against the timestamp
data['IP'] = data['IP'].astype(str)
axs[1].plot(data['TIME_STAMP'], data['IP'])
axs[1].set_xlabel('TIME_STAMP')
axs[1].set_ylabel('IP')
axs[1].set_title('IP addresses over time')
axs[1].tick_params(rotation=45)

# Plot the throughput values against the timestamp
axs[2].plot(data['TIME_STAMP'], data['DL Throughput [Mbps]'])
axs[2].set_xlabel('TIME_STAMP')
axs[2].set_ylabel('Throughput')
axs[2].set_title('Throughput values over time')
axs[2].tick_params(rotation=45)

# Adjust the spacing between subplots
plt.tight_layout()

# Show the plots
plt.show()
