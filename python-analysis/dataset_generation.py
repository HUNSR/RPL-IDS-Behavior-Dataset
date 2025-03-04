import csv
import os
import pandas as pd

import numpy as np
SIMULATION_TIME = 72000  # Change this value as needed in second
AGGREGATION_INTERVAL = 1 #  1 minutes

def shuffle_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)  # Read the CSV into a DataFrame
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle the rows
    df.to_csv(output_csv, index=False)  # Write the shuffled DataFrame back to CSV
    print(f"Shuffled and saved the CSV file: {output_csv}")

def process_cooja_log(log_file,  simulation_minutes= SIMULATION_TIME):
    # Dictionary to store information for each node with intervals as keys
    output_file= 'temp.txt'
    node_data = {}

    with (open(log_file, 'r') as file):
        for line in file:
            # Only process lines that contain "ids:"
            if "ids:" in line:
                parts = line.split("ids:")

                # Extract timestamp, main node ID, and info string
                time_node_part = parts[0].strip().split()
                timestamp = int(time_node_part[0])  # Convert timestamp to integer
                main_node_id = int(time_node_part[1])  # Main node ID as integer
                info_string = parts[1].strip()  # Information after "ids:"

                # Split the main node info and the other nodes' info
                main_info, *neighbor_nodes_info = info_string.split(':')
                if main_info.endswith(","):
                    main_info = main_info[:-1]

                tempid= int(main_info.split(',')[0])
                if tempid != main_node_id:
                    print("error")
                    continue
                # Determine minute interval based on timestamp
                interval = timestamp // ((AGGREGATION_INTERVAL * 60000000)) # 60000000 = 1 minutes assuming timestamp in microseconds

                # Initialize node_data entry for main node if not exists
                if main_node_id not in node_data:
                    node_data[main_node_id] = {}

                # Ensure each interval has a list to store data segments
                if interval not in node_data[main_node_id]:
                    node_data[main_node_id][interval] = [f"{interval},{main_info}"]
    file.close()

    with (open(log_file, 'r') as file):
        for line in file:
            # Only process lines that contain "ids:"
            if "ids:" in line:
                parts = line.split("ids:")

                # Extract timestamp, main node ID, and info string
                time_node_part = parts[0].strip().split()
                timestamp = int(time_node_part[0])  # Convert timestamp to integer
                main_node_id = int(time_node_part[1])  # Main node ID as integer
                if(main_node_id == 0 ):
                    print("break \n")
                info_string = parts[1].strip()  # Information after "ids:"

                # Split the main node info and the other nodes' info
                main_info, *neighbor_nodes_info = info_string.split(':')

                # Determine minute interval based on timestamp
                interval = timestamp // ((AGGREGATION_INTERVAL * 60000000)) # 60000000 = 1 minutes assuming timestamp in microseconds

                # Process each neighbor node info if present
                for neighbor_info in neighbor_nodes_info:
                    # Skip empty or invalid neighbor entries (e.g., just `$`)
                    neighbor_info = neighbor_info.strip(';$').strip()
                    if not neighbor_info:
                        continue

                    neighbor_info_parts = neighbor_info.split(";")

                    for neighbor_info_part in neighbor_info_parts:

                    # Separate the neighbor node ID from the rest of its data
                        neighbor_data = neighbor_info_part.split(',')
                        try:
                            neighbor_node_id = int(neighbor_data[0])
                        except ValueError:
                            continue  # Skip if neighbor ID is invalid
                        neighbor_data = [str(main_node_id)] + neighbor_data[1:]



                        # Format data for the neighbor node
                        formatted_neighbor_info = ','.join(neighbor_data)

                        # Initialize neighbor node in node_data if not present
                        if neighbor_node_id not in node_data:
                            node_data[neighbor_node_id] = {}
                        if interval not in node_data[neighbor_node_id]:
                            node_data[neighbor_node_id][interval] = []

                        # Append this information to the corresponding neighbor node
                        node_data[neighbor_node_id][interval].append(f";{formatted_neighbor_info}")

    # Write the processed data to the output file
    with open(output_file, 'w') as out_file:
        for interval in range(simulation_minutes//60):  # 60 minutes => 60 intervals
            for node_id in sorted(node_data.keys()):
                # Check if there is data for this interval for this node
                if interval in node_data[node_id]:
                    # Join multiple records in the interval with a space, if any
                    record = ''.join(node_data[node_id][interval])
                    out_file.write(f"{record}\n")
                # else:
                #     # Write anneighbor_values empty entry if no data for this interval
                #     out_file.write(f"{interval},{node_id},NA\n")

def generate_csv( output_file, write_header=True):
    import csv
    import numpy as np

    input_file = 'temp.txt'

    # with open(input_file, mode="r") as infile, open(output_file, mode="w", newline="") as csvfile:
    #     writer = csv.writer(csvfile)

    with open(input_file, mode="r") as infile, open(output_file, mode="a" if not write_header else "w",
                                                    newline="") as csvfile:
        writer = csv.writer(csvfile)

        if write_header:
            header = [
                "time_sec", "node_id", "parent_id", "rpl_ver", "rpl_rank",
                "dis_sent", "dio_sent", "dao_sent",
                "nbr_dis_rcv", "nbr_dio_rcv", "nbr_dao_ack_rcv",
                "nbr_fwd_to_me", "nbr_fwd_to_others", "nbr_fwd_bcast",
                "nbr_rpl_ctrl", "nbr_non_rpl_ctrl",
                "nbr_rpl_ver_rcv", "nbr_rpl_rank_rcv",
                "nbr_fwd_rpl", "nbr_fwd_non_rpl",
                "diff_rpl_rank", "diff_rpl_ver",
                "norm_rank_diff", "ctrl_to_data_ratio",
                "non_rpl_to_rpl_ratio",
                "rpl_fwd_ratio", "non_rpl_fwd_ratio", "total_fwd_ratio",
                "label"
            ]
            writer.writerow(header)

        # Read each line from the input file
        for line in infile:
            line = line.strip()
            if not line or "NA" in line:
                continue

            # Split line by ";" to separate main info and neighbor info
            parts = line.split(";")

            # Ensure there is main info
            if len(parts) < 2:
                continue

            # Extract main node info and ensure it has at least 11 fields
            main_info = parts[0].split(",")
            if len(main_info) < 11:
                continue

            try:
                # Parse main node info
                time_sec = int(main_info[0])
                node_id = int(main_info[1])
                parent_id = int(main_info[2])
                RPL_version = int(main_info[3])
                RPL_rank = int(main_info[4])
                DIS_sent = int(main_info[5])
                DIO_sent = int(main_info[6])
                DAO_sent = int(main_info[7])
                label = int(main_info[10])

                main_node_info = [
                    time_sec, node_id, parent_id, RPL_version, RPL_rank,
                    DIS_sent, DIO_sent, DAO_sent
                ]
            except ValueError:
                continue

            # Initialize neighbor data collection
            neighbor_data = []

            # Process each neighbor's info
            for neighbor in parts[1:]:
                neighbor_fields = neighbor.split(",")
                if len(neighbor_fields) >= 13:  # Ensure neighbor info length
                    try:
                        neighbor_values = list(map(int, neighbor_fields[1:14]))
                        neighbor_data.append(neighbor_values)
                    except ValueError:
                        continue

            if neighbor_data:
                # Convert to numpy array for easier manipulation
                neighbor_data = np.array(neighbor_data)

                # Calculate averages, ignoring zero values
                neighbor_avg = []
                for col in range(neighbor_data.shape[1]):
                    non_zero_values = neighbor_data[:, col][neighbor_data[:, col] != 0]
                    avg_value = int(np.mean(non_zero_values)) if len(non_zero_values) > 0 else 0
                    neighbor_avg.append(avg_value)
            else:
                neighbor_avg = [0] * 13

            # Calculate forwarding ratios
            RPL_forwarding_ratio = neighbor_avg[6] / neighbor_avg[10] if neighbor_avg[10] > 0 else 0
            Non_RPL_forwarding_ratio = neighbor_avg[7] / neighbor_avg[11] if neighbor_avg[11] > 0 else 0
            forwarding_ratio = RPL_forwarding_ratio + Non_RPL_forwarding_ratio

            # Write the updated row to the CSV
            writer.writerow(main_node_info + neighbor_avg + [
                abs(RPL_rank - neighbor_avg[9]) if RPL_rank and neighbor_avg[9] else 0,   # abs_diff_RPL_rank
                abs(RPL_version - neighbor_avg[8]) if RPL_version and neighbor_avg[8] else 0,   # abs_diff_RPL_version
                abs(RPL_rank - neighbor_avg[9]) / max(RPL_rank, neighbor_avg[9]) if RPL_rank and neighbor_avg[9] else 0,  # normalized_rank_diff
                (DIS_sent + DIO_sent + DAO_sent) / neighbor_avg[6] if neighbor_avg[6] > 0 else 0,  # ratio_of_control_to_data_packets
                neighbor_avg[7] / neighbor_avg[6] if neighbor_avg[6] > 0 else 0,  # ratio_Non_RPL_control_to_RPL_control
                RPL_forwarding_ratio, Non_RPL_forwarding_ratio, forwarding_ratio,
                label
            ])

# Define folder paths and output file names
log_folder = 'dataset'
output_csv = 'RPL-IDS-Beh.csv'

# Iterate over all files in the log folder and its subfolders
first_file = True
for root, _, files in os.walk(log_folder):
    for log_file in files:
        if log_file.startswith("cooja"):  # Check if the file name starts with "COOJA"
            log_path = os.path.join(root, log_file)  # Get the full file path
            print(f"Processing file: {log_path}")
            process_cooja_log(log_path, )  # Process the log file
            generate_csv( output_csv, write_header=first_file)  # Generate the CSV
            first_file = False  # Write the header only for the first file

shuffle_csv(output_csv, output_csv)
