import nltk
import random

# 下载词库
nltk.download('words')

from nltk.corpus import words

# 获取所有英文单词
word_list = words.words()

def generate_word_en():
    return random.choice(word_list)


for i in range(2000000):  # 获取200w个单词
    word = generate_word_en()
    # print(word)
    with open ("random_word.txt", "a", encoding="utf-8") as f:
        f.write(word + "\n")

# 去重
with open("random_word.txt", "r", encoding="utf-8") as f:
    words = [line.strip() for line in f.readlines()]
    words = list(set(words))
    print(len(words))
    with open("random_word.txt", "w", encoding="utf-8") as f:
        for word in words:
            f.write(word + "\n")
