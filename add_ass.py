# -*- coding: utf-8 -*-

import os
import subprocess
def add_ass_to_video(video_file, ass_file):
    if not os.path.isfile(video_file):
        print(f"Error: Input video_file file '{video_file}' does not exist.")
        return
    if not os.path.isfile(ass_file):
        print(f"Error: Input ass_file file '{ass_file}' does not exist.")
        return

    if os.path.isfile(video_file + "_with_ass.mp4"):
        print(f"Error: Output video file '{video_file + '_with_ass.mp4'}' already exists.")
        return

    ffmpeg_command = [
        "ffmpeg",
        "-hwaccel", "videotoolbox",
        "-i", video_file,
        "-vf", f"ass={ass_file}",
        "-c:v", "h264_videotoolbox",
        "-c:a", "copy",
        video_file + "_with_ass.mp4"
    ]
    print(f"开始处理: -> {video_file}")
    subprocess.run(ffmpeg_command)
    print(f"处理完成: -> {video_file}")

ass_dir = "1to4/3/ass2"
video_dir = "1to4/3/listen/video"

# convert_mp3_to_video("1to4/4/listen/4-L1-L2_1.mp3", "blackboard.jpg", "1to4/4/listen/video/4-L1-L2_1.mp4")

#
for filename in os.listdir(video_dir):
    if filename.endswith(".mp4"):
        mp4_file = os.path.join(video_dir, filename)
        ass_file = os.path.join(ass_dir, os.path.splitext(filename)[0] + ".ass")
        add_ass_to_video(mp4_file, ass_file)
