import csv
from datetime import datetime, timedelta

file_name = 'm3-Queens.csv'

# Output file
output_file_name = 'm3-Queens_A2A_output'
ap_to_ap_time_list = []


# Open the CSV file and write
def write_to_csv(row_to_write):
    with open('/Users/P2982820/Desktop/' + output_file_name + '.csv', 'a') as csvfile:
        # writing row to the output csv
        csvfile.writelines(row_to_write)

# Write in txt file
def write_to_txt(row_to_write):
    with open('/Users/P2982820/Desktop/' + output_file_name + '.txt', 'a') as txt_file:
        # writing row to the output txt
        txt_file.write(row_to_write)

# Read data from csv
with open('/Users/P2982820/Desktop/' + file_name, 'r') as file:
    # Create a CSV reader
    reader = csv.DictReader(file)

    # Initialize variables
    previous_mac = None
    previous_timestamp = None
    previous_state = None
    previous_rssi = None
    start_rssi = None
    end_rssi = None
    new_mac, completed_new_mac = False, False
    start_time = None
    end_time = None

    # Iterate over the rows in the CSV file
    for row in reader:
        #print(row)
        # break

        state = row['Supplicant State']
        try:
            timestamp = row['TIME_STAMP']
        except:
            timestamp = row['\ufeffTIME_STAMP']
        try:
            tp_dl = float(row['DL Throughput [Mbps]'])
        except:
            tp_dl = 0
        row_MAC = row['BSSID']
        row_RSSI = row['RSSI']

        # print(MAC_change)
        # break

        # Store previous state,mac, and timestamp

        # Check if the state is completed"
        if state == 'COMPLETED':
            previous_state = state
            previous_mac = row_MAC
            previous_rssi = row_RSSI

        # Set the start time if it has not been set yet
        if tp_dl > 0 and previous_state == 'COMPLETED' and not new_mac:
            start_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            start_rssi = previous_rssi
            # Setting MAC for validating Complete is from the same MAC
            # MAC = row_MAC
            # print(row)
            # print(tp_dl)

            # #temporary reset
            # start_time, end_time, MAC = None, None, None
            # previous_timestamp, previous_state, previous_state = None, None, None

        # new_ap flag
        if (state == 'ASSOCIATED' or state == 'ASSOCIATING') and previous_mac != row_MAC:
            new_mac = True
        if state == 'COMPLETED' and new_mac:
            completed_new_mac = True
            end_rssi = row_RSSI

        # Check if the state is "COMPLETED" after "ASSOCIATING and throughput is greater than zero"
        elif state == '' and tp_dl > 0 and start_time is not None and completed_new_mac:  # and timestamp >= end_time_c:
            end_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            # print(f'TIME: {timestamp}, TP_DL = {tp_dl}Mb')
            time_difference = end_time - start_time
            print(
                f'Start Time: {start_time}, Start RSSI: {start_rssi}, End RSSI: {end_rssi}, End Time: {timestamp}'
                f'TP_DL = {tp_dl}Mb | Time between AP to AP, {time_difference}')

            ap_to_ap_time_list.append(time_difference)

            # writing to csv file
            write_to_csv(
                f'Start Time: {start_time}, Start RSSI: {start_rssi}, End RSSI: {end_rssi}, End Time: {timestamp} TP_DL = {tp_dl}Mb | Time between AP to AP, {time_difference}\n')

            # with open('/Users/P2982820/Desktop/' + output_file_name, 'a') as csvfile:
            #     # writing row to the output csv
            #     csvfile.writelines(
            #         f'Start Time: {start_time}, Start RSSI: {start_rssi}, End RSSI: {end_rssi}, End Time: {timestamp}'
            #         f'TP_DL = {tp_dl}Mb | Time between AP to AP, {time_difference}\n')
            write_to_txt(
                f'Start Time: {start_time}, Start RSSI: {start_rssi}, End RSSI: '
                f'{end_rssi}, End Time: {timestamp} TP_DL = {tp_dl}Mb | Time between AP to AP, {time_difference}\n')
            # # writing to txt file
            # with open('/Users/P2982820/Desktop/' + output_file_name + 'txt', 'a') as txt_file:
            #     # writing row to the output txt
            #     txt_file.write(
            #         f'Start Time: {start_time}, Start RSSI: {start_rssi}, End RSSI: {end_rssi}, End Time: {timestamp}'
            #         f'TP_DL = {tp_dl}Mb | Time between AP to AP, {time_difference}\n')

            # Resetting start and end time
            start_time, end_time, MAC = None, None, None
            previous_timestamp, previous_state, previous_state = None, None, None
            start_rssi, end_rssi, previous_rssi = None, None, None
            new_mac, completed_new_mac = False, False


def Average(lst):
    return sum(lst, timedelta()) / len(lst)

average = Average(ap_to_ap_time_list)
print(f' , , , Average:,{average}')
write_to_csv(f' , , , Average:,{average}')
write_to_txt(f' , , , Average:,{average}')
