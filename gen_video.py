# -*- coding: utf-8 -*-

import os
import subprocess
def convert_mp3_to_video(mp3_file, image_file, output_file):
    if not os.path.isfile(mp3_file):
        print(f"Error: Input MP3 file '{mp3_file}' does not exist.")
        return
    if not os.path.isfile(image_file):
        print(f"Error: Input image file '{image_file}' does not exist.")
        return
    if os.path.isfile(output_file):
        print(f"Error: Output video file '{output_file}' already exists.")
        return

    ffmpeg_command = [
        "ffmpeg",
        "-hwaccel", "videotoolbox",
        "-loop", "1",
        "-i", image_file,
        "-i", mp3_file,
        "-c:v", "h264_videotoolbox",
        "-c:a", "aac",
        "-shortest",
        output_file
    ]
    print(f"开始处理: {filename} -> {output_file}")
    subprocess.run(ffmpeg_command)
    print(f"处理完成: {filename} -> {output_file}")
    # ffmpeg_command = [
    #     "ffmpeg",
    #     "-i", output_file,
    #     "-vf", "subtitles='{}.lrc':force_style='FontSize=40,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BackColour=&H00000000,Outline=1,Shadow=0,MarginL=10,MarginR=10,MarginV=10'".format(os.path.splitext(output_file)[0]),
    #     "-c:v", "libx264",
    #     "-c:a", "copy",
    #     output_file
    # ]
    # subprocess.run(ffmpeg_command)
input_dir = "1to4/3/listen"
output_dir = "1to4/3/listen/video"


#
for filename in os.listdir(input_dir):
    if filename.endswith(".mp3"):
        mp3_file = os.path.join(input_dir, filename)
        image_file = "blackboard.png"
        output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".mp4")
        convert_mp3_to_video(mp3_file, image_file, output_file)
