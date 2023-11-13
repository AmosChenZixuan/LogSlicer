import os
import numpy as np
from sklearn.cluster import KMeans

from langchain.docstore.document import Document
from langchain.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()


def plot(vectors, kmeans):
    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt
    import numpy as np

    # Perform t-SNE and reduce to 2 dimensions
    tsne = TSNE(n_components=2, random_state=42)
    reduced_data_tsne = tsne.fit_transform(np.array(vectors))

    # Plot the reduced data
    plt.scatter(reduced_data_tsne[:, 0], reduced_data_tsne[:, 1], c=kmeans.labels_)
    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.title('Chunk Embeddings Clusters')
    plt.show()


def chunk_select(chunks: [Document], num_clusters=3):

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("CHATGPT_API_KEY"))

    vectors = embeddings.embed_documents([x.page_content for x in chunks])
    kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(vectors)

    plot(vectors, kmeans)

    closest_indices = []

    for i in range(num_clusters):
        distances = np.linalg.norm(vectors - kmeans.cluster_centers_[i], axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append(closest_index)

    selected_indices = sorted(closest_indices)
    return [chunks[i] for i in selected_indices]