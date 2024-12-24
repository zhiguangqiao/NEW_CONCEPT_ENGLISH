def process_text_file(input_file, output_file, encoding='utf-8'):
    # 读取文本文件内容
    with open(input_file, 'r', encoding=encoding) as f:
        content = f.read().strip()  # 去掉多余的换行符

    # 以空行分割内容为数组
    sections = content.split('\n\n')

    if len(sections) < 3:
        raise ValueError("输入文件内容格式不正确，至少需要三个部分")

    # 获取标题，英文原文和中文翻译
    title = sections[0].strip()
    english_text = sections[2].strip()
    chinese_text = sections[-1].strip()

    # 按句号分割为句子
    english_sentences = [sentence.strip() + '.' for sentence in english_text.split('.') if sentence.strip()]
    chinese_sentences = [sentence.strip() + '。' for sentence in chinese_text.split('。') if sentence.strip()]

    # 确保中英文句子数量一致
    if len(english_sentences) != len(chinese_sentences):
        print(english_sentences, chinese_sentences,flush=True)
        raise ValueError("英文句子和中文句子数量不匹配")

    # 写入到新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入标题
        f.write(title + '\n\n')

        # 写入中英文句子
        for eng, chi in zip(english_sentences, chinese_sentences):
            f.write(eng + '\n')
            f.write(chi + '\n\n')

# 调用示例
input_file = '1to4/3/1.TXT'  # 输入文件名
output_file = 'output.txt'  # 输出文件名
process_text_file(input_file, output_file, encoding='gbk')
print("文件处理完成，结果已写入：", output_file)
