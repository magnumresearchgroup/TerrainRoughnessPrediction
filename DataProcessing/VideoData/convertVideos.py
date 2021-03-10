"""
This python script uses cv2 to capture a video from the local directory
and then it extracts each frame from the recording. We can easily modify this to loop
through many mp4 files. Additionally, the output of the number of frames is dependent
on the fps of the video itself. The timing can be modified for the frames extracted.
"""

import cv2
import os

dictionaryUTC = {
    "2020-07-28-06-01-11": [964868527, 713],
    "2020-09-24-1": [969901730, 242],
    "2020-09-24-2": [969903230, 694],
    "2020-09-24-3": [969904731, 180],
    "2020-09-24-4": [969906231, 665],
    "2020-09-23-VIRB0001": [969829854, 741],
    "2020-09-23-VIRB0002": [969829956, 258],
    "2020-09-23-VIRB0004": [969830811, 205],
    "2020-09-23-VIRB0008": [969832325, 654],
    "2020-09-29-09-46-42-1": [970325257, 797],
    "2020-09-29-09-46-42-2": [970326758, 215],
    "2020-09-29-09-46-42-3": [970328258,	701],
    "2020-09-29-09-46-42-4": [970329759,	186],
    "2020-10-02-10-17-05-1": [970586258, 96],
    "2020-10-02-10-17-05-2": [970587758, 498],
    "2020-10-02-10-17-05-3": [970588070, 257],
}

def get_frames(video, title, name, folder):
    # capturing video from local directory
    cap = cv2.VideoCapture(folder + ".MP4")

    # frame per second for video
    # additional video information
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("FPS:", fps)
    if(fps == 0):
        return

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(round(frame_count / fps, 0))
    ms_bet_frames = 1000.0 / fps

    print("Video duration:", duration, "s")
    print("ms between frames:", ms_bet_frames, "ms")

    framenums = []
    # getting the appropriate frame number
    for i in range(0, duration + 1):
        ms = i * 1000
        frame_num = ms / ms_bet_frames
        framenums.append(int(round(frame_num, 0)))

    # loop through video
    i = 0
    counter = 0
    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        # save frame per one second interval
        # dependent on fps (in this case, the first frame of every second)
        if (counter < len(framenums)) and i == framenums[counter]:
            frame_time = framenums[counter] / fps
            ms = int(round((frame_time - int(frame_time)) * 1000, 0))

            # Add the video's UTC start time to label with UTC timestamp
            utc_s = int(frame_time) + dictionaryUTC[title][0]
            utc_ms = ms + dictionaryUTC[title][1]
            if utc_ms >= 1000:
                utc_s += 1
                utc_ms = utc_ms % 1000

            image_name = str(utc_s) + 's' + str(utc_ms) + 'ms.jpg'
            cv2.imwrite(os.path.join(folder, image_name), frame)
            counter += 1

            if counter % 10 == 0:
                print("....", counter, "/", duration, "frames generated....")

        i += 1

    # clean up
    cap.release()
    cv2.destroyAllWindows()

def main():
    video_path = ""
    for file in os.listdir(video_path):
        filename = os.fsdecode(file)
        if filename.endswith(".MP4"):
            print("Found the following MP4 file:" + filename)
            endIndex = filename.index(".MP4")
            title = filename[0:endIndex]
            if title in dictionaryUTC:
                folder = os.path.join(video_path, str(title))
                if not os.path.isdir(folder):
                    os.mkdir(folder)
                print("Processing " + title)
                get_frames(video=filename, title=title, name=title, folder=folder)


if __name__ == "__main__":
    main()

