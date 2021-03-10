import csv
import os
import pandas as pd


def append_video_start_times(filename, folder, utc_con_s, utc_con_ms, video_information):
    start_times = []
    end_times = []

    csv_file = open(filename, "rt")
    reader = csv.DictReader(csv_file)

    # Camera events:
    # 0     video_start
    # 1     video_split
    # 2     video_end

    for row in reader:
        if row["Type"] == "Data" and row["Message"] == "camera_event":
            sys_s = int(row["Value 1"])
            sys_ms = int(row["Value 3"])
            camera_event_type = int(row["Value 4"])

            if camera_event_type == 0:
                start_times.append((sys_s, sys_ms))
            elif camera_event_type == 2:
                end_times.append((sys_s, sys_ms))
            elif camera_event_type == 1:
                start_times.append((sys_s, sys_ms))
                end_times.append((sys_s, sys_ms))

    if len(start_times) != len(end_times):
        print("The number of start times does not correspond to the number of end times.")
        return

    for i in range(0, len(start_times)):
        start_s = start_times[i][0]
        start_ms = start_times[i][1]
        end_s = end_times[i][0]
        end_ms = end_times[i][1]

        elapsed_s = end_s - start_s
        elapsed_ms = end_ms - start_ms
        if elapsed_ms < 0:
            elapsed_ms += 1000
            elapsed_s -= 1

        utc_s = start_s + utc_con_s
        utc_ms = start_ms + utc_con_ms
        if utc_ms >= 1000:
            utc_s += 1
            utc_ms %= 1000

        video_row = {
            "session": folder,
            "video_id": i,
            "utc_start_s": utc_s,
            "utc_start_ms": utc_ms,
            "start_s": start_s,
            "start_ms": start_ms,
            "end_s": end_s,
            "end_ms": end_ms,
            "elapsed_s": elapsed_s,
            "elapsed_ms": elapsed_ms
        }

        video_information = video_information.append(video_row, ignore_index=True)

    return video_information


def get_utc_conversion_factor(filename, folder):
    csv_file = open(filename, "rt")
    reader = csv.DictReader(csv_file)

    for row in reader:
        if row["Type"] == "Data" and row["Message"] == "timestamp_correlation":
            utc_s = int(float(row["Value 1"]))
            utc_ms = int(float(row["Value 4"]))
            sys_s = int(float(row["Value 2"]))
            sys_ms = int(float(row["Value 5"]))
            if ((utc_ms - sys_ms) < 0):
                con_s = utc_s - 1 - sys_s
                con_ms = utc_ms + 1000 - sys_ms
            else:
                con_s = utc_s - sys_s
                con_ms = utc_ms - sys_ms

            conv_row = {
                "session": folder,
                "utc_con_s": con_s,
                "utc_con_ms": con_ms,
                "sys_s": sys_s,
                "sys_ms": sys_ms,
                "utc_s": utc_s,
                "utc_ms": utc_ms,
            }

            csv_file.close()
            return conv_row

    csv_file.close()
    return []


def main():

    # If running this script for every session, leave lines 109 - 112 uncommented.
    conversion_factors = pd.DataFrame(columns=["session", "utc_con_s", "utc_con_ms", "sys_s", "sys_ms",
                                               "utc_s", "utc_ms"])
    video_information = pd.DataFrame(columns=["session", "video_id", "utc_start_s", "utc_start_ms", "start_s",
                                              "start_ms", "end_s", "end_ms", "elapsed_s", "elapsed_ms"])

    # If running this script to append data to the existing CSVs:
    #   1. Comment lines 109 and 111
    #   2. Uncomment lines 119, 120, and 121
    #   3. Add "if folder == <folderName>" below line 125, where folderName is the folder with the data
    #       you would like to add.
    # csv_path = ""
    # conversion_factors = pd.read_csv(os.path.join(csv_path,"utc_conversion_factors.csv"), index_col=False)
    # video_information = pd.read_csv(os.path.join(csv_path, "video_information.csv"), index_col=False)

    # Change this to the file path
    filePath = ""
    for subdir, dirs, files in os.walk(filePath):
        for folder in dirs:
            absolute_path = os.path.join(subdir, folder)
            other_file = os.path.join(absolute_path, "other.csv")
            conv_row = get_utc_conversion_factor(other_file, folder)
            conversion_factors = conversion_factors.append(conv_row, ignore_index=True)
            video_information = append_video_start_times(other_file, folder, conv_row["utc_con_s"],
                                                         conv_row["utc_con_ms"], video_information)

    # Add path to save CSVs
    conversion_factors.to_csv("")
    video_information.to_csv("")


if __name__ == "__main__":
    main()
