import csv
from datetime import datetime

file_name = 'm2_toyota.csv'
# file_name = 'm2_new.csv'

# Output file
output_file_name = 'm2_toyota_legacy_output.csv'

# Open the CSV file
with open('/Users/P2982820/Desktop/' + file_name, 'r') as file:
    # Create a CSV reader
    reader = csv.DictReader(file)

    # Initialize variables
    start_time = None
    end_time = None
    MAC = None
    MAC_change = None

    # measure the time between state changed to first "ASSOCIATING" to "COMPLETED" 
    # Iterate over the rows in the CSV file
    for row in reader:
        # print(row)
        # break

        state = row['Supplicant State']
        try:
            timestamp = row['TIME_STAMP']
        except:
            timestamp = row['\ufeffTIME_STAMP']
        tp_dl = row['DL Throughput [Mbps]']
        row_MAC = row['BSSID']
        ip = row['IP']


        # Capture MAC for completed session for overlapping scenario
        if state == 'COMPLETED':
            MAC_change = row_MAC
            # print(MAC_change)
            # break
        # Check if the state is "ASSOCIATING or ASSOCIATED with IP"
        if state == 'ASSOCIATING':
            # Set the start time if it has not been set yet

            if start_time is None:
                start_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
                # Setting MAC for validating Complete is from the same MAC
                MAC = row_MAC


        # # Check ASSOCIATED
        # if state == 'ASSOCIATED' and ip != '0.0.0.0' and MAC_change != row_MAC:
        #     # Set the start time if it has not been set yet
        #
        #     if start_time is None:
        #         start_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        #         # Setting MAC for validating Complete is from the same MAC
        #         print(MAC_change, row_MAC, row)
        #         MAC_change = row_MAC

        # Check if the state is "COMPLETED" after "ASSOCIATING from the same MAC"
        elif (state == 'COMPLETED' and start_time is not None and row_MAC != MAC) or state == 'DISCONNECTED':
            # Resetting start and end time
            start_time, end_time, MAC = None, None, None

            #     end_time_c = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')

        # Check if the state is "COMPLETED" after "ASSOCIATING and throughput is greater than zero"
        elif state == '' and tp_dl != '0' and start_time is not None:  # and timestamp >= end_time_c:
            end_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            # print(f'TIME: {timestamp}, TP_DL = {tp_dl}Mb')
            time_difference = end_time - start_time
            print(
                f'TIME: {timestamp}, TP_DL = {tp_dl}Mb | Time between ASSOCIATING and the first byte, {time_difference}')

            # writing to csv file
            with open('/Users/P2982820/Desktop/' + output_file_name, 'a') as csvfile:
                # writing row to the output csv
                csvfile.writelines(
                    f'TIME: {timestamp}, TP_DL = {tp_dl}Mb | ime between ASSOCIATING and the first byte, {time_difference}\n')

                # Resetting start and end time
            start_time, end_time, MAC, MAC_change = None, None, None, None


