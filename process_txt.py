import os

def process_text_file(input_file, output_file):
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
    english_text = sections[2].strip()
    english_text = re.sub(r"U\.S\.", "U S ", english_text)
    chinese_text = sections[-1].strip()

    # 处理生词表
    new_words_sections = sections[4:-2]
    new_words_dict = {}
    if len(new_words_sections) > 0:
        new_words_lines = new_words_sections
        for line in new_words_lines:
            match = re.match(r"\s*(\S.*?)\s+[nv\.]+\s+(.*)", line)
            if match:
                word, meaning = match.groups()
                new_words_dict[word.strip()] = meaning.strip()

    # 按句号分割为句子
    english_sentences = [sentence.strip() + '.' for sentence in english_text.split('.') if sentence.strip()]
    chinese_sentences = [sentence.strip() + '。' for sentence in chinese_text.split('。') if sentence.strip()]

    # 确保中英文句子数量一致
    if len(english_sentences) != len(chinese_sentences):
        print(f"英文句子数量：{len(english_sentences)}")
        print(f"中文句子数量：{len(chinese_sentences)}")
        print(input_file)
        for eng, chi in zip(english_sentences, chinese_sentences):
            print(eng, chi)
        raise ValueError("英文句子和中文句子数量不匹配")

    # 写入到新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入标题
        f.write(title + '\n\n')

        # 写入中英文句子，添加生词
        for eng, chi in zip(english_sentences, chinese_sentences):
            # 提取句子中的生词
            words_in_sentence = [word for word in new_words_dict if word in eng]
            word_line = ''
            for word in words_in_sentence:
                word_line += f"{word}: {new_words_dict[word]}, "
            word_line = word_line.strip(', ')
            if len(word_line) > 0:
                f.write(word_line + '\n')
            f.write(eng + '\n')
            f.write(chi + '\n\n')

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path):
            output_path = os.path.join(output_dir, f"output_{filename}")
            try:
                process_text_file(input_path, output_path)
                print(f"处理完成: {filename} -> {output_path}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错:")

# 调用示例
input_dir = '1to4/4/ass'  # 输入文件夹
input_dir_txt = '1to4/4/txt'  # 输入文件夹
process_directory(input_dir, output_dir)
print("所有文件处理完成。")

