import csv
import shutil
from tempfile import NamedTemporaryFile
import glob
import os
import pandas as pd
import numpy as np


# Set up an output folder for a given unfiltered CSV file and return the folder directory
def setup_output_directory(folder_location, filename):
    path, name = os.path.split(filename)
    folder_name = os.path.splitext(name)[0]
    if '-calibrated' in folder_name:
        folder_name = folder_name.replace('-calibrated', '')
    folder_directory = os.path.join(folder_location, folder_name)

    if not os.path.isdir(folder_directory):
        os.mkdir(folder_directory)

    return folder_directory


# Given a filtered DataFrame and list of columns, create a formatted CSV
def filtered_data_to_csv(filtered_data, filename, fields, column_names):
    if filtered_data.empty:
        print(".... No data exists for this sensor ....")
        return

    df = pd.DataFrame(columns=fields)

    new_rows = []
    for index, row in filtered_data.iterrows():
        insert_row = {}
        for field in fields:
            insert_row[field] = None

        for i in range(0, len(row)):
            if row[i] in insert_row:
                insert_row[row[i]] = row[i + 1]

        new_rows.append(insert_row)

    df = df.append(new_rows, ignore_index=True)
    df.columns = column_names

    df.to_csv(filename, index=False)


# Create pandas DataFrame object holding the data corresponding to the different calibrated sensor readings
def calibrated_df_from_csv(filename):
    data = pd.read_csv(filename)
    
    accel_data_cal = data[
        np.logical_and(
            data['Message'] == 'accelerometer_data',
            data['Type'] == 'Data'
        )
    ]
    accel_data_cal = accel_data_cal.dropna(axis='columns', how='all')
    
    gyroscope_data_cal = data[
        np.logical_and(
            data['Message'] == 'gyroscope_data',
            data['Type'] == 'Data'
        )
    ]
    gyroscope_data_cal = gyroscope_data_cal.dropna(axis='columns', how='all')
    
    return accel_data_cal, gyroscope_data_cal


# Call filtered_data_to_csv for the data from each sensor using the calibrated readings
def generate_calibrated_csvs(folder_directory, filename):
    accel_data_cal, gyroscope_data_cal = calibrated_df_from_csv(filename)
    
    print(".... Generating calibrated acceleration data CSV ....")
    accel_fields = ['timestamp', 'timestamp_ms', 'sample_time_offset', 'accel_x', 'accel_y', 'accel_z', 'calibrated_accel_x', 'calibrated_accel_y', 'calibrated_accel_z']
    accel_column_names = ['timestamp (s)', 'timestamp_ms (ms)', 'sample_time_offset (ms)', 'accel_x (counts)', 'accel_y (counts)', 'accel_z (counts)', 'calibrated_accel_x (g)', 'calibrated_accel_y (g)', 'calibrated_accel_z (g)']
    filtered_data_to_csv(accel_data_cal, folder_directory + "/accelerometer_calibrated.csv", accel_fields, accel_column_names)

    print(".... Generating calibrated gyroscope data CSV ....")
    gyro_fields = ['timestamp', 'timestamp_ms', 'sample_time_offset', 'gyro_x', 'gyro_y', 'gyro_z', 'calibrated_gyro_x', 'calibrated_gyro_y', 'calibrated_gyro_z']
    gyro_column_names = ['timestamp (s)', 'timestamp_ms (ms)', 'sample_time_offset (ms)', 'gyro_x (counts)', 'gyro_y (counts)', 'gyro_z (counts)', 'calibrated_gyro_x (deg/s)', 'calibrated_gyro_y (deg/s)', 'calibrated_gyro_z (deg/s)']
    filtered_data_to_csv(gyroscope_data_cal, folder_directory + "/gyroscope_calibrated.csv", gyro_fields, gyro_column_names)


# Create pandas DataFrame objects holding the data corresponding to the different messages
def df_from_csv(filename):
    data = pd.read_csv(filename)

    gps_data = data[
        np.logical_and(
            data['Message'] == 'gps_metadata',
            data['Type'] == 'Data'
        )
    ]
    gps_data = gps_data.dropna(axis='columns', how='all')

    magnetometer_data = data[
        np.logical_and(
            data['Message'] == 'magnetometer_data',
            data['Type'] == 'Data'
        )
    ]
    magnetometer_data = magnetometer_data.dropna(axis='columns', how='all')

    record_data = data[
        np.logical_and(
            data['Message'] == 'record',
            data['Type'] == 'Data'
        )
    ]
    record_data = record_data.dropna(axis='columns', how='all')

    other_data = data[
        np.logical_and.reduce([
            data['Message'] != 'accelerometer_data',
            data['Message'] != 'gps_metadata',
            data['Message'] != 'gyroscope_data',
            data['Message'] != 'magnetometer_data',
            data['Message'] != 'record'
        ])
    ]
    other_data = other_data.dropna(axis='columns', how='all')

    return gps_data, magnetometer_data, record_data, other_data


# Call filtered_data_to_csv for the data from each sensor
def generate_all_csvs(folder_directory, filename):
    gps_data, magnetometer_data, record_data, other_data = df_from_csv(filename)

    print(".... Generating GPS data CSV ....")
    gps_fields = ['timestamp', 'timestamp_ms', 'position_lat', 'position_long', 'enhanced_altitude',
                  'enhanced_speed', 'utc_timestamp', 'heading', 'velocity']
    gps_column_names = ['timestamp (s)', 'timestamp_ms (ms)', 'position_lat (semicircles)',
                        'position_long (semicircles)', 'enhanced_altitude (m)', 'enhanced_speed (m/s)',
                        'utc_timestamp (s)', 'heading (degrees)', 'velocity (m/s)']
    filtered_data_to_csv(gps_data, folder_directory + "/gps.csv", gps_fields, gps_column_names)

    print(".... Generating magnetometer data CSV ....")
    magnet_fields = ['timestamp', 'timestamp_ms', 'sample_time_offset', 'mag_x', 'mag_y', 'mag_z']
    magnet_column_names = ['timestamp (s)', 'timestamp_ms (ms)', 'sample_time (ms)', 'mag_x (counts)',
                           'mag_y (counts)', 'mag_z (counts)']
    filtered_data_to_csv(magnetometer_data, folder_directory + "/magnetometer.csv", magnet_fields, magnet_column_names)

    print(".... Generating record data CSV ....")
    record_fields = ['timestamp', 'position_lat', 'position_long', 'distance', 'enhanced_speed', 'enhanced_altitude']
    record_column_names = ['timestamp (s)', 'position_lat (semicircles)','position_long (semicircles)',
                           'distance (m)', 'enhanced_speed (m/s)', 'enhanced_altitude (m)']
    filtered_data_to_csv(record_data, folder_directory + "/record.csv", record_fields, record_column_names)

    print(".... Generating CSV with data from other message types ....")
    other_data.to_csv(folder_directory + "/other.csv", index=False)


def main():
    # Replace with the location of the raw Virb CSV files on your machine
    original_files = glob.glob("")
    # Output directory
    original_output = ""
    for filename in original_files:
        folder_directory = setup_output_directory(original_output, filename)
        print("\nGenerating filtered CSV files for file: " + folder_directory + "\n")
        generate_all_csvs(folder_directory, filename)

    # Replace with the location of the raw calibrated Virb CSV files on your machine
    calibrated_files = glob.glob("")
    calibrated_output = ""
    for filename in calibrated_files:
        folder_directory = setup_output_directory(calibrated_output, filename)
        print("\nGenerating calibrated filtered CSV files for file: " + folder_directory + "\n")
        generate_calibrated_csvs(folder_directory, filename)

if __name__ == "__main__":
    main()
