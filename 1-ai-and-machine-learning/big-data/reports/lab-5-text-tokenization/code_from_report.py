# Code extracted from the lab report (report.pdf)

# ---- fragment 1 ----
import urllib.request
url = ("https://raw.githubusercontent.com/rasbt/"
"LLMs-from-scratch/main/ch02/01_main-chapter-code/"
"the-verdict.txt")
file_path = "the-verdict.txt"
urllib.request.urlretrieve(url, file_path)

# ---- fragment 2 ----
with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
print("Total number of character:", len(raw_text))
print(raw_text[:99])

# ---- fragment 3 ----
import re

with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
print("Кількість токенів: ", len(preprocessed))
print("Перші 30 токенів: ", preprocessed[:30])

# ---- fragment 4 ----
all_words = sorted(set(preprocessed))
vocab_size = len(all_words)
print(vocab_size)

vocab = {token:integer for integer,token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    print(item)
    if i >= 50:
        break

# ---- fragment 5 ----
class SimpleTokenizerV1:
    def __init__(self, vocab):
        self.str_to_int = vocab
        self.int_to_str = {i:s for s,i in vocab.items()}

    def encode(self, text):
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        preprocessed = [
        item.strip() for item in preprocessed if item.strip()
        ]
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids

    def decode(self, ids):
        text = " ".join([self.int_to_str[i] for i in ids])
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text

# ---- fragment 6 ----
preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
all_words = sorted(set(preprocessed))
vocab = {token:integer for integer,token in enumerate(all_words)}

class SimpleTokenizerV1:
    def __init__(self, vocab):
        self.unk_token = "<UNK>"

        if self.unk_token not in vocab:
            vocab[self.unk_token] = len(vocab)

        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}

    def encode(self, text):
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', text)
        preprocessed = [item.strip() for item in preprocessed if item.strip()]

        ids = []
        for token in preprocessed:
            if token in self.str_to_int:
                ids.append(self.str_to_int[token])
            else:
                ids.append(self.str_to_int[self.unk_token])
        return ids

    def decode(self, ids):
        text = " ".join([self.int_to_str.get(i, self.unk_token) for i in ids])
        text = re.sub(r'\s+([,.?!"()\'])', r'\1', text)
        return text

# ---- fragment 7 ----
tokenizer = SimpleTokenizerV1(vocab)

encode = tokenizer.encode(raw_text)
print("Кодування: ", encode)
print("Декодування: ", tokenizer.decode(encode))

text = "Hello, lorem dolore augue?"

encode = tokenizer.encode(text)
print("Кодування: ", encode)
print("Декодування: ", tokenizer.decode(encode))

# ---- fragment 8 ----
print("\nТЕСТ 1: Пробіли vs Без пробілів\n")
sample_words = preprocessed[:10]
sentence_with_spaces = " ".join(sample_words)
sentence_no_spaces = "".join(sample_words)

tokens_with_spaces = tokenizer.encode(sentence_with_spaces)
tokens_no_spaces = tokenizer.encode(sentence_no_spaces)

print("Текст з пробілами:\n", sentence_with_spaces)
print("К-сть токенів:", len(tokens_with_spaces))
print("Токени:", tokens_with_spaces)

print("\nТекст без пробілів:\n", sentence_no_spaces)
print("К-сть токенів:", len(tokens_no_spaces))
print("Токени:", tokens_no_spaces)

print("\nТЕСТ 2: Регістр vs lower()\n")
sentence_case = " ".join(preprocessed[:12])

tokens_case = tokenizer.encode(sentence_case)

pre_lower = [t.lower() for t in preprocessed]
vocab_lower = {tok: i for i, tok in enumerate(sorted(set(pre_lower)))}
tokenizer_lower = SimpleTokenizerV1(vocab_lower)

tokens_case_lower = tokenizer_lower.encode(sentence_case.lower())

print("Оригінальна фраза:")
print(sentence_case)
print("\nОригінальні токени:", tokens_case)

print("\nФраза в lower:")
print(sentence_case.lower())
print("Lower токени:", tokens_case_lower)

print("\nРозмір словника з регістром:", len(vocab))
print("Розмір словника без регістру (lower):", len(vocab_lower))

print("\nТЕСТ 3: Пунктуація vs Без пунктуації\n")
sentences = re.split(r'[.!?]', raw_text)
sentence_raw = sentences[0].strip()

sentence_no_punct = re.sub(r'[,.:;!?()"\'-]', '', sentence_raw)

tokens_punct = tokenizer.encode(sentence_raw)
tokens_no_punct = tokenizer.encode(sentence_no_punct)

print("Фраза з пунктуацією:")
print(sentence_raw)
print("Токени:", tokens_punct)

print("\nФраза без пунктуації:")
print(sentence_no_punct)
print("Токени:", tokens_no_punct)
