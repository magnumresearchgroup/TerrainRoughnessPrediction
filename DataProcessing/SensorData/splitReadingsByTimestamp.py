import csv
import shutil
from tempfile import NamedTemporaryFile
import os


def proAccelCal(subdir, file):
    csv_file = open(os.path.join(subdir, file), "rt")
    with open(subdir + '/accelerometer_calibrated_split.csv', 'wb') as new_file:
        reader = csv.DictReader(csv_file)
        fieldname = ['timestamp (s)', 'timestamp_ms (ms)', 'accel_x (counts)',
                     'accel_y (counts)', 'accel_z (counts)', 'calibrated_accel_x (g)',
                     'calibrated_accel_y (g)', 'calibrated_accel_z (g)', 'calibrated_accel_x (m/s^2)',
                     'calibrated_accel_y (m/s^2)', 'calibrated_accel_z (m/s^2)']

        writer = csv.DictWriter(new_file, fieldnames=fieldname)
        writer.writeheader()

        for row in reader:
            msParse = [row['sample_time_offset (ms)'].split('|'), row['accel_x (counts)'].split('|'),
                       row['accel_y (counts)'].split('|'), row['accel_z (counts)'].split('|'),
                       row['calibrated_accel_x (g)'].split('|'), row['calibrated_accel_y (g)'].split('|'),
                       row['calibrated_accel_z (g)'].split('|')]

            for period in range(len(msParse[0])):
                time_ms = int(float(row['timestamp_ms (ms)'])) + int(msParse[0][period])
                time_s = int(float(row['timestamp (s)']))
                if time_ms >= 1000:
                    time_ms = time_ms % 1000
                    time_s += 1
                writer.writerow({
                    'timestamp (s)': time_s,
                    'timestamp_ms (ms)': time_ms,
                    'accel_x (counts)': msParse[1][period],
                    'accel_y (counts)': msParse[2][period],
                    'accel_z (counts)': msParse[3][period],
                    'calibrated_accel_x (g)': msParse[4][period],
                    'calibrated_accel_y (g)': msParse[5][period],
                    'calibrated_accel_z (g)': msParse[6][period],
                    'calibrated_accel_x (m/s^2)': 9.80665 * float(msParse[4][period]),
                    'calibrated_accel_y (m/s^2)': 9.80665 * float(msParse[5][period]),
                    'calibrated_accel_z (m/s^2)': 9.80665 * float(msParse[6][period]),
                })
    csv_file.close()
    new_file.close()


def proGyroCal(subdir, file):
    csv_file = open(os.path.join(subdir, file), "rt")
    with open(subdir + '/gyroscope_calibrated_split.csv', 'wb') as new_file:
        reader = csv.DictReader(csv_file)
        fieldname = ['timestamp (s)', 'timestamp_ms (ms)', 'gyro_x (counts)',
                    'gyro_y (counts)', 'gyro_z (counts)', 'calibrated_gyro_x (deg/s)',
                     'calibrated_gyro_y (deg/s)', 'calibrated_gyro_z (deg/s)']
        writer = csv.DictWriter(new_file, fieldnames=fieldname)
        writer.writeheader()

        for row in reader:
            msParse = [row['sample_time_offset (ms)'].split('|'), row['gyro_x (counts)'].split('|'),
                       row['gyro_y (counts)'].split('|'), row['gyro_z (counts)'].split('|'),
                       row['calibrated_gyro_x (deg/s)'].split('|'), row['calibrated_gyro_y (deg/s)'].split('|'),
                       row['calibrated_gyro_z (deg/s)'].split('|')]

            for period in range(len(msParse[0])):
                time_ms = int(float(row['timestamp_ms (ms)'])) + int(msParse[0][period])
                time_s = int(float(row['timestamp (s)']))
                if time_ms >= 1000:
                    time_ms = time_ms % 1000
                    time_s += 1
                writer.writerow({
                    'timestamp (s)': time_s,
                    'timestamp_ms (ms)': time_ms,
                    'gyro_x (counts)': msParse[1][period],
                    'gyro_y (counts)': msParse[2][period],
                    'gyro_z (counts)': msParse[3][period],
                    'calibrated_gyro_x (deg/s)': msParse[4][period],
                    'calibrated_gyro_y (deg/s)': msParse[5][period],
                    'calibrated_gyro_z (deg/s)': msParse[6][period],
                })
    csv_file.close()
    new_file.close()
    

def proMagn(subdir, file):
    csv_file = open(os.path.join(subdir, file), "rt")
    with open(subdir + '/magnetometer_split.csv', 'wb') as new_file:
        reader = csv.DictReader(csv_file)
        fieldname = ['timestamp (s)', 'timestamp_ms (ms)', 'mag_x (counts)',
                          'mag_y (counts)', 'mag_z (counts)']
        writer = csv.DictWriter(new_file, fieldnames=fieldname)
        writer.writeheader()

        for row in reader:
            msParse = [row['sample_time (ms)'].split('|'), row['mag_x (counts)'].split('|'),
                       row['mag_y (counts)'].split('|'), row['mag_z (counts)'].split('|')]
            for period in range(len(msParse[0])):
                time_ms = int(float(row['timestamp_ms (ms)'])) + int(msParse[0][period])
                time_s = int(float(row['timestamp (s)']))
                if time_ms >= 1000:
                    time_ms = time_ms % 1000
                    time_s += 1
                writer.writerow({
                    'timestamp (s)': time_s,
                    'timestamp_ms (ms)': time_ms,
                    'mag_x (counts)': msParse[1][period],
                    'mag_y (counts)': msParse[2][period],
                    'mag_z (counts)': msParse[3][period]
                })
    csv_file.close()
    new_file.close()


def main():
    # change this path to the directory which contains all the folders of data
    filePath = ""
    for subdir, dirs, files in os.walk(filePath):
        for file in files:
            _, folder = os.path.split(subdir)
            if file == "magnetometer.csv":
                print("\nprocessing: " + os.path.join(folder, file))
                proMagn(subdir, file)
            elif file == "accelerometer_calibrated.csv":
                print("\nprocessing: " + os.path.join(folder, file))
                proAccelCal(subdir, file)
            elif file == "gyroscope_calibrated.csv":
                print("\nprocessing: " + os.path.join(folder, file))
                proGyroCal(subdir, file)


if __name__ == "__main__":
    main()
