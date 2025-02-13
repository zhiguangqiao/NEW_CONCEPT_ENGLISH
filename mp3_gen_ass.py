# coding:utf-8
import sys

import whisper
# from moviepy.audio.io.AudioFileClip import AudioFileClip
# from mutagen.mp3 import MP3
from googletrans import Translator
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_key.json'

translator = Translator()


def translate_text(text, src="en", dest="zh-cn"):
    try:
        result = translator.translate(text, src=src, dest=dest)
        return result.text
    except Exception as e:
        print(f"翻译失败: {e}")
        return text

def generate_ass_from_transcription(transcriptions, ass_file):
    """
    根据转录文本生成带中文翻译的 ASS 字幕文件。

    Args:
        transcriptions (list): 转录的结果，包含 (开始时间, 结束时间, 文本) 的元组。
        ass_file (str): 输出的 ASS 字幕文件路径。
        translator (Translator): googletrans 翻译器对象。
    """
    # 创建 ASS 文件头部
    ass_header = """[Script Info]
Title: Generated Subtitle
Original Script: Python Script
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
WrapStyle: 3

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,PingFang SC,18,&H00FFFFFF,&H00FFFFFF,&H0037FFFF,&HFF000000,0,1,0,0,100,100,0,0,1,1,0,4,20,20,20,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    # 创建 ASS 字幕内容
    ass_events = ""
    for start, end, text in transcriptions:
        start_time = format_ass_time(start)
        end_time = format_ass_time(end)
        translated_text = translate_text(text)
        combined_text = f"{text}\\N\\N{translated_text}"
        ass_events += f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{combined_text}\n"

    # 写入 ASS 文件
    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ass_header)
        f.write(ass_events)

    print(f"字幕文件生成成功: {ass_file}")


def format_ass_time(seconds):
    """将秒数转换为 ASS 时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:01}:{minutes:02}:{secs:05.2f}"


def transcribe_mp3_to_ass(mp3_file, ass_file, model):
    if os.path.exists(ass_file):
        print(f"Error: Output ass_file file '{ass_file}' already exists.")
        return

    # 使用 Whisper 转录音频
    print(f"正在转录文件: {mp3_file}，请稍候...")
    result = model.transcribe(mp3_file, language="en")
    segments = result['segments']

    # 提取转录结果
    transcriptions = []
    for segment in segments:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        transcriptions.append((start, end, text))

    # 生成 ASS 字幕文件
    generate_ass_from_transcription(transcriptions, ass_file)


def batch_process_mp3_to_ass(input_dir, output_dir, model_name="medium.en"):
    # 检查输入输出目录
    if not os.path.exists(input_dir):
        print(f"输入目录 {input_dir} 不存在！")
        return
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    model = whisper.load_model(model_name)

    # 遍历输入目录中的 MP3 文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".mp3"):
            mp3_path = os.path.join(input_dir, file_name)
            ass_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + ".ass")
            transcribe_mp3_to_ass(mp3_path, ass_path, model)


if __name__ == "__main__":

    input_directory = "1to4/3/listen/test"
    output_directory = "1to4/3/ass"

    # 如果没有输入参数，或参数为空字符串则报错退出
    if not input_directory or not output_directory:
        print("请输入输入目录和输出目录！")
        exit(1)

    # 入股 input_directory 不存在，则打印错误退出
    if not os.path.exists(input_directory):
        print(f"输入目录 {input_directory} 不存在！")
        exit(1)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 批量处理 MP3 文件
    batch_process_mp3_to_ass(input_directory, output_directory)
