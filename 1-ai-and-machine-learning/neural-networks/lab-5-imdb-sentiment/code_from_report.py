# Code extracted from the lab report (report.pdf)

# ---- fragment 1 ----
class IMDBDataset(Dataset):
    def __init__(self, split):
        self.data = dataset[split]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.data[idx]["text"]
        label = self.data[idx]["label"]
        encoding = tokenizer(text, truncation=True, padding="max_length", max_length=128, return_tensors="pt")
        return encoding["input_ids"].squeeze(0), encoding["attention_mask"].squeeze(0), torch.tensor(label, dtype=torch.long)

Значить ось прописаний класс IMDBDataset. Клас створений щоб підготувати текстові дані (IMDB) у форматі з яким може працювати PyTorch-модель.

# ---- fragment 2 ----
class LSTMWithAttention(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, output_dim):
        super(LSTMWithAttention, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.attn = nn.Linear(hidden_dim * 4, hidden_dim)
        self.v = nn.Parameter(torch.rand(hidden_dim))
        self.fc = nn.Linear(hidden_dim * 2, output_dim)

    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        hidden = lstm_out[:, -1, :].unsqueeze(1).repeat(1, lstm_out.shape[1], 1)
        concat = torch.cat((hidden, lstm_out), dim=2)
        energy = torch.tanh(self.attn(concat)).matmul(self.v)
        attn_weights = torch.softmax(energy, dim=1)
        context_vector = torch.sum(attn_weights.unsqueeze(2) * lstm_out, dim=1)
        return self.fc(context_vector), attn_weights

# ---- fragment 3 ----
vocab_size = tokenizer.vocab_size - кількість унікальних токенів у словнику токенізатора.
embed_dim = 128  -  розмірність
hidden_dim = 256 - кількість нейронів у прихованому шарі LSTM.
output_dim = 2 - кількість класів

lstm_model = LSTMWithAttention(vocab_size, embed_dim, hidden_dim, output_dim).to(device)
lstm_optimizer = optim.Adam(lstm_model.parameters(), lr=2e-4)

def compute_metrics_lstm(model, loader):
