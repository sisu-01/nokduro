import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def visualize_dbscan(features, labels):
    """
    DBSCAN 결과를 2D 도표로 시각화.
    
    :param features: 외곽선 특징 배열 (numpy 배열, shape: [n_samples, 2])
    :param labels: DBSCAN으로 클러스터링한 결과의 레이블 배열
    """

    # y 값을 반전해서 시각화용 데이터 생성
    inverted_features = features.copy()
    inverted_features[:, 1] *= -1  # y 값 반전

    # 유일한 라벨 값 가져오기
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]

    # 시각화
    plt.figure(figsize=(8, 4))
    for label, color in zip(unique_labels, colors):
        if label == -1:
            # 노이즈는 검은색으로 표시
            color = [0, 0, 0, 1]

        class_member_mask = (labels == label)
        xy = inverted_features[class_member_mask]

        plt.scatter(xy[:, 0], xy[:, 1], c=[color], label=f"Cluster {label}" if label != -1 else "Noise", s=50)
    
    plt.title("DBSCAN Clustering Results (Monitor Graphics)")
    plt.xlabel("X Coordinate (0 to 1920)")
    plt.ylabel("Y Coordinate (0 to 1080, Inverted)")
    plt.xlim(0, 1920)
    plt.ylim(-1080, 0)  # y값 반전으로 인해 -1080이 아래, 0이 위로 표시
    plt.legend(loc="upper right", bbox_to_anchor=(1.2, 1), title="Clusters")
    plt.grid()
    plt.show()