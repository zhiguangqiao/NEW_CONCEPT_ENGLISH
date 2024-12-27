# -*- coding: utf-8 -*-

import os
import re

def lrc_to_srt(lrc_path, srt_path):
    with open(lrc_path, 'r', encoding='gbk') as lrc_file:
        lines = lrc_file.readlines()

    srt_entries = []
    entry_index = 1

    for line in lines:
        # 匹配 LRC 时间戳和歌词
        match = re.match(r'\[(\d+):(\d+)\.(\d+)\](.*)', line)
        if match:
            minutes = int(match.group(1))
            seconds = int(match.group(2))
            milliseconds = int(match.group(3)) * 10  # 毫秒是两位数，需要乘以10
            text = match.group(4).strip()

            # 计算时间戳
            start_time = f"{minutes:02}:{seconds:02},{milliseconds:03}"

            # 获取下一行时间戳作为结束时间
            next_line = lines[lines.index(line) + 1] if lines.index(line) + 1 < len(lines) else None
            end_time = "99:59:59,999"  # 默认结束时间
            if next_line:
                next_match = re.match(r'\[(\d+):(\d+)\.(\d+)\]', next_line)
                if next_match:
                    next_minutes = int(next_match.group(1))
                    next_seconds = int(next_match.group(2))
                    next_milliseconds = int(next_match.group(3)) * 10
                    end_time = f"{next_minutes:02}:{next_seconds:02},{next_milliseconds:03}"

            # 创建 SRT 条目
            srt_entries.append(f"{entry_index}\n{start_time} --> {end_time}\n{text}\n")
            entry_index += 1

    # 写入 SRT 文件
    with open(srt_path, 'w', encoding='utf-8') as srt_file:
        srt_file.writelines(srt_entries)

def batch_convert_lrc_to_srt(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith('.lrc'):
            lrc_path = os.path.join(input_dir, filename)
            srt_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.srt')
            lrc_to_srt(lrc_path, srt_path)
            print(f"Converted: {lrc_path} -> {srt_path}")

# 使用示例
input_directory = '1to4/4/listen'  # 输入目录，存放 LRC 文件

batch_convert_lrc_to_srt(input_directory, input_directory)
