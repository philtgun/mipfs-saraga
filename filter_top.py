from pathlib import Path
import os
import pandas as pd

import config

root_path = os.path.join(config.DATA_PATH, config.PREPROCESS_DIR)
data = []
for raga_dir in os.listdir(root_path):
    raga_path = os.path.join(root_path, raga_dir)
    paths = list(Path(raga_path).rglob("*.mp3"))
    data.append({'raga': raga_dir, 'total': len(paths)})

df = pd.DataFrame(data)
df = df.sort_values(by='total', ascending=False)
print(df[:10])
