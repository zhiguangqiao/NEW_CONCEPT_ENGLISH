# -*- coding: utf-8 -*-

import os
from gtts import gTTS

def process_text_file(input_file, output_file):
    if os.path.isfile(output_file):
        print(f"Error: Output video file '{output_file}' already exists.")
        return
    import re

    # 读取文本文件内容
    with open(input_file, 'r', encoding='gbk') as f:
        content = f.read().strip()  # 去掉多余的换行符
    content = re.sub(r"\n\s+\n", "\n\n", content)
    # 以空行分割内容为数组
    sections = content.split('\n\n')

    if len(sections) < 3:
        raise ValueError("输入文件内容格式不正确，至少需要三个部分")

    # 获取标题，英文原文和中文翻译
    title = sections[0].strip()

    lines = title.splitlines()

    # 保留不包含中文的行
    filtered_lines = [line for line in lines if not re.search(r'[\u4e00-\u9fff]', line)]

    # 合并过滤后的行
    title = "\n".join(filtered_lines)

    english_text = sections[2].strip()
    tts = gTTS(title + '\n' + english_text, lang="en")  # 设置语言为中文（可以自动处理中英文混合）
    tts.save(output_file)

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path) and filename.endswith('.txt'):
            output_path = os.path.join(output_dir, filename + '.mp3')
            try:
                process_text_file(input_path, output_path)
                print(f"处理完成: {filename} -> {output_path}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错:")

# 调用示例
input_dir = '1to4/3'  # 输入文件夹
output_dir = '1to4/3/text'  # 输出文件夹
process_directory(input_dir, output_dir)
print("所有文件处理完成。")

