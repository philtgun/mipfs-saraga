import os

import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

import config

data = np.load(os.path.join(config.DATA_PATH, 'test_embed.npy'))
labels = np.load(os.path.join(config.DATA_PATH, 'test_label.npy'))
raga_labels = [
    'begada',
    'behag',
    'bhairavi',
    'kamas',
    'kamboji',
    'kedaragaula',
    'kuntalavarali',
    'riti gaula',
    'shri',
    'thodi'
]

# data_emb = TSNE().fit_transform(data)
data_emb = np.load('emb.npy')

fig, ax = plt.subplots()
scatter = ax.scatter(data_emb[:, 0], data_emb[:, 1], c=labels)
print(scatter.legend_elements())

legend1 = ax.legend(*scatter.legend_elements(), #raga_labels,
                    loc="upper left", title="Ragas")
ax.add_artist(legend1)

plt.savefig('plot.png', bbox_inches='tight')
plt.show()
