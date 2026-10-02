"""CPU throughput of a small Phoenix-like ranker (the 'L1' stand-in).

Architecture mirrors Phoenix at toy scale: user history (item id + category + action) as a
sequence, candidate tokens that attend to history but not to each other (candidate isolation),
multi-head sigmoid outputs (click, long_view, like, follow, comment, forward, hate).
Synthetic batches sized like KuaiRand-1K; we only time it.
"""
import time, torch, torch.nn as nn
torch.set_num_threads(4); torch.manual_seed(0)
N_ITEMS, N_CATS, N_ACT, N_HEADS = 200_000, 70, 8, 7   # items hashed into 200k buckets
HIST, CANDS, D, B = 128, 16, 64, 256

class Ranker(nn.Module):
    def __init__(s, layers=2):
        super().__init__()
        s.item = nn.Embedding(N_ITEMS, D); s.cat = nn.Embedding(N_CATS, D); s.act = nn.Embedding(N_ACT, D)
        s.pos = nn.Embedding(HIST + CANDS, D)
        s.enc = nn.TransformerEncoder(nn.TransformerEncoderLayer(D, 4, 4 * D, batch_first=True, dropout=0.0), layers)
        s.head = nn.Linear(D, N_HEADS)
        L = HIST + CANDS; m = torch.zeros(L, L, dtype=torch.bool)
        m[:HIST, HIST:] = True                         # history does not see candidates
        m[HIST:, HIST:] = ~torch.eye(CANDS, dtype=torch.bool)   # candidate isolation
        s.register_buffer('mask', m)
    def forward(s, hi, hc, ha, ci, cc):
        h = s.item(hi) + s.cat(hc) + s.act(ha); c = s.item(ci) + s.cat(cc)
        x = torch.cat([h, c], 1) + s.pos.weight
        return s.head(s.enc(x, mask=s.mask)[:, HIST:])

for layers in (2, 4):
    m = Ranker(layers); opt = torch.optim.AdamW(m.parameters(), 1e-3); lossf = nn.BCEWithLogitsLoss()
    def batch():
        return (torch.randint(0, N_ITEMS, (B, HIST)), torch.randint(0, N_CATS, (B, HIST)), torch.randint(0, N_ACT, (B, HIST)),
                torch.randint(0, N_ITEMS, (B, CANDS)), torch.randint(0, N_CATS, (B, CANDS)), torch.rand(B, CANDS, N_HEADS).round())
    for it in range(23):
        if it == 3: t0 = time.time()
        *x, y = batch(); loss = lossf(m(*x), y); opt.zero_grad(); loss.backward(); opt.step()
    dt = (time.time() - t0) / 20; per_s = B * CANDS / dt
    n_par = sum(p.numel() for p in m.parameters())
    print(f'{layers} layers, d={D}, hist={HIST}, {n_par/1e6:.1f}M params: {dt*1000:.0f} ms/step -> {per_s:,.0f} labelled candidates/s; '
          f'one epoch of KuaiRand-1K standard logs (~11.7M) ~ {11.7e6/per_s/60:.0f} min')
