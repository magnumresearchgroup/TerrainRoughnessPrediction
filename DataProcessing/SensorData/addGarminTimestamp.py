import os
import pandas as pd

def main():
    # change this path to the directory which contains all the folders of data
    filePath = ""
    for subdir, dirs, files in os.walk(filePath):
        for dir in dirs:
            absolute_path = os.path.join(subdir, dir)
            record_file = os.path.join(absolute_path, "record.csv")
            
            record_df = pd.read_csv(record_file)
            record_df['utc_s (s)'] = record_df['timestamp (s)']
            record_df['utc_ms (ms)'] = [0 for _ in range(len(record_df))]
            
            record_df = record_df.filter(items=['utc_s (s)', 'utc_ms (ms)', 'timestamp (s)', 'position_lat (semicircles)', 'position_long (semicircles)', 'distance (m)', 'enhanced_speed (m/s)', 'enhanced_altitude (m)'])
            
            record_df.to_csv(os.path.join(absolute_path, "record.csv"))


if __name__ == "__main__":
    main()

