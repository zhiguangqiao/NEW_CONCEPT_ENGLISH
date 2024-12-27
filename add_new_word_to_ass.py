# coding:utf-8
import os
import re

from lrc_to_ass import get_word_dict


def add_word_list_to_ass(input_ass_file, output_ass_file, word_map):
    """
    给 ASS 文件中的每行英文字幕前增加一行生词列表。
    """
    with open(input_ass_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    new_lines = []
    dialogue_pattern = re.compile(r"^Dialogue:.*?,(\d+:\d+:\d+\.\d+),(\d+:\d+:\d+\.\d+),.*?,.*?,.*?,.*?,.*?,.*?,(.*)")

    for line in lines:
        # 识别字幕行
        match = dialogue_pattern.match(line)
        if match:
            start_time, end_time, text = match.groups()
            # 提取英文字幕（假定字幕行的英文在首行）
            english_text = re.split(r"\\N|\n", text)[0]

            # 根据 word_map 提取生词
            words_in_line = [word for word in word_map if word in english_text]
            if words_in_line:
                word_list = ", ".join([f"{word}: {word_map[word]}" for word in words_in_line])
                # 添加生词列表为新的一行
                word_list_line = f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,, {word_list}\\N\\N{text}\n"
                new_lines.append(word_list_line)
            else:
                new_lines.append(line)
        else:
            # 无论是否匹配都保留原始行
            new_lines.append(line)

    # 写入新的 ASS 文件
    with open(output_ass_file, "w", encoding="utf-8") as outfile:
        outfile.writelines(new_lines)


if __name__ == '__main__':
    input_folder = '1to4/3/ass'
    new_word_folder = '1to4/3/'
    output_folder = '1to4/3/ass2'
    if not os.path.exists(new_word_folder):
        os.makedirs(new_word_folder)
    for f in os.listdir(input_folder):
        if f.lower().endswith('.ass'):
            input_ass_file = os.path.join(input_folder, f)
            output_ass_file = os.path.join(output_folder, f)
            new_word_file = os.path.join(new_word_folder, f.replace('.ass', '.txt'))
            word_map = get_word_dict(new_word_file)
            add_word_list_to_ass(input_ass_file, output_ass_file, word_map)

