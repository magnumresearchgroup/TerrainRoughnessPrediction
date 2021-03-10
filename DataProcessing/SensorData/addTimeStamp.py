import csv
import os
import pandas as pd

def addTime(filename, con_time):
    csv_name = os.path.split(filename)[1]
    df = pd.read_csv(filename)
    
    cols = df.columns
    if 'utc_s (s)' in cols or 'utc_ms (ms)' in cols:
        print(csv_name + " already has UTC timestamps.")
        return

    utc_s_list = df['timestamp (s)'] + con_time[0]
    if csv_name != 'record.csv':
        utc_ms_list = df['timestamp_ms (ms)'] + con_time[1]
    else:
        utc_ms_list = pd.Series([0 for _ in range(0, len(utc_s_list))])

    carry_indices = utc_ms_list >= 1000
    utc_ms_list[carry_indices] = utc_ms_list % 1000
    utc_s_list[carry_indices] += 1

    df.insert(loc=0, column='utc_s (s)', value=utc_s_list)
    df.insert(loc=1, column='utc_ms (ms)', value=utc_ms_list)

    df.to_csv(filename)


def get_utc_conversion_factor(filename):
    csv_file = open(filename, "rt")
    reader = csv.DictReader(csv_file)

    for row in reader:
        if row["Type"] == "Data" and row["Message"] == "timestamp_correlation":
            utc_s = int(float(row["Value 1"]))
            utc_ms = int(float(row["Value 4"]))
            sys_s = int(float(row["Value 2"]))
            sys_ms = int(float(row["Value 5"]))
            if ((utc_ms - sys_ms) < 0):
                con_s = utc_s - 1 -sys_s
                con_ms = utc_ms + 1000 - sys_ms
            else:
                con_s = utc_s - sys_s
                con_ms = utc_ms - sys_ms
            csv_file.close()

            print("\nFilename: " + filename)
            print("UTC timestamp: " + str(utc_s) + " s, " + str(utc_ms) + " ms")
            print("System timestamp: " + str(sys_s) + " s, " + str(sys_ms) + " ms")
            print("UTC conversion factor: " + str(con_s) + " s, " + str(con_ms) + " ms")

            return [con_s, con_ms]

    csv_file.close()
    return []


def main():
    dont_add_utc = ['other.csv', 'magnetometer.csv', 'accelerometer_calibrated.csv', 'gyroscope_calibrated.csv']

    # change this path to the directory which contains all the folders of data
    filePath = ""
    for subdir, dirs, files in os.walk(filePath):
        for dir in dirs:
            absolute_path = os.path.join(subdir, dir)
            other_file = os.path.join(absolute_path, "other.csv")
            convertion_time = get_utc_conversion_factor(other_file)
            for subdir_dir, dirs_dir, files_dir in os.walk(absolute_path):
                for file_dir in files_dir:
                    if file_dir not in dont_add_utc:
                        filename = os.path.join(subdir_dir, file_dir)
                        print(".... Processing: " + os.path.join(dir, file_dir) + " ....")
                        addTime(filename, convertion_time)


if __name__ == "__main__":
    main()
