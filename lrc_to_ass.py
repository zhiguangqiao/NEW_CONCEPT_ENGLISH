
# coding: utf-8
import os
import re

def get_word_dict(text_file):
    with open(text_file, 'r', encoding='gbk') as f:
        content = f.read().strip()  # 去掉多余的换行符
    content = re.sub(r"\n\s+\n", "\n\n", content)
    new_words_dict = {}
    if len(content) > 0:
        matches = re.findall(r" {4}(\S.*?)\n([a-z]+\. +\S+)\n", content)
        for match in matches:
            if match:
                word, meaning = match
                new_words_dict[word.strip()] = meaning.strip()
    return new_words_dict

def lrc_to_ass(lrc_file, text_file,ass_file):
    """将单个 LRC 文件转换为 ASS 文件"""
    ass_header = """[Script Info]
Title: Converted from LRC
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0
WrapStyle: 3

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,PingFang SC,20,&H00FFFFFF,&H00FFFFFF,&H0037FFFF,&HFF000000,0,1,0,0,100,100,0,0,1,1,0,4,50,50,50,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    lrc_pattern = re.compile(r"\[(\d{2}):(\d{2}\.\d{2})\](.*)")
    subtitles = []
    new_words_dict = get_word_dict(text_file)
    with open(lrc_file, 'r', encoding='gbk') as file:
        for line in file:
            match = lrc_pattern.match(line.strip())
            if match:
                minutes, seconds, text = match.groups()
                start_time = int(minutes) * 60 + float(seconds)
                subtitles.append((start_time, text.strip()))

    ass_events = []
    for i, (start_time, text) in enumerate(subtitles):
        start_time_str = format_ass_time(start_time)
        end_time = subtitles[i + 1][0] if i + 1 < len(subtitles) else start_time + 5
        end_time_str = format_ass_time(end_time)
        text = text.replace('\\n', '\\N\\N')
        words_in_sentence = [word for word in new_words_dict if word in text]
        word_line = ''
        for word in words_in_sentence:
            word_line += f"{word}: {new_words_dict[word]}, "
        if len(word_line) > 0:
            text = word_line.strip(', ') + '\\N\\N' + text
        ass_events.append(f"Dialogue: 0,{start_time_str},{end_time_str},Default,,0,0,0,,{text}")

    with open(ass_file, 'w', encoding='utf-8') as file:
        file.write(ass_header)
        file.write("\n".join(ass_events))

    print(f"已转换: {lrc_file} -> {ass_file}")


def format_ass_time(seconds):
    """将秒数转换为 ASS 时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:01}:{minutes:02}:{secs:05.2f}"


def batch_convert_lrc_to_ass(input_folder, txt_folder, output_folder):
    """批量将文件夹中的 LRC 文件转换为 ASS 文件"""
    if not os.path.isdir(input_folder):
        print(f"输入的路径不是文件夹: {input_folder}")
        return

    # 获取所有 .lrc 文件
    lrc_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.lrc')]
    if not lrc_files:
        print("未找到任何 LRC 文件。")
        return
    lrc_files.sort(key=lambda x: (len(x), x))
    for index, lrc_file in enumerate(lrc_files):
        text_file = os.path.join(txt_folder,  f"{index + 1}.TXT")
        lrc_path = os.path.join(input_folder, lrc_file)
        ass_path = os.path.join(output_folder, os.path.splitext(lrc_file)[0] + '.ass')
        lrc_to_ass(lrc_path, text_file,ass_path)

    print("批量转换完成！")


# 示例用法
if __name__ == "__main__":
    input_folder = "1to4/4/listen"  # 替换为你的 LRC 文件夹路径
    batch_convert_lrc_to_ass(input_folder, "1to4/4", "1to4/4/ass")
