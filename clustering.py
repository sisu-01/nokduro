from sklearn.cluster import DBSCAN
from graphics import visualize_dbscan
from utils import average_centers, check_labels, average_contour_coordinates
import numpy as np
import cv2

MIN_SAMPLES = 2

# 각 군집이 빨간 점과 파란 점을 모두 포함하는지 확인하는 함수
# def filter_clusters(labels, cluster_labels, color_labels):
#   filtered_clusters = []
#   unique_clusters = np.unique(cluster_labels)
  
#   for cluster in unique_clusters:
#       if cluster == -1:  # 노이즈는 제외
#           continue
#       cluster_points = labels[cluster_labels == cluster]
#       # 빨간 점(0)과 파란 점(1)이 모두 포함된 군집만 필터링
#       if np.any(cluster_points == 0) and np.any(cluster_points == 1):
#           filtered_clusters.append(cluster)
  
#   return filtered_clusters

def cluster_contour_features(features, colors, image, EPS=10):
  dbscan = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES)  # eps와 min_samples는 데이터에 따라 조정
  dbscan_labels = dbscan.fit_predict(features)

  # 필터링 - 빨간 점과 파란 점이 함께 있는 군집만 남김
  valid_clusters = []
  for cluster_id in set(dbscan_labels):
    if cluster_id == -1:  # 노이즈 제외
      continue
    cluster_indices = np.where(dbscan_labels == cluster_id)[0]
    cluster_colors = [colors[i] for i in cluster_indices]
    # 빨간 점과 파란 점이 모두 포함된 경우만 유효
    if 'white' in cluster_colors and 'black' in cluster_colors:
      black_count = cluster_colors.count('black')
      white_count = cluster_colors.count('white')
      if white_count > black_count / 20 and (black_count > 5 and white_count > 5):
        #test = white_count / black_count * 100
        #print(f'{int(test)}, black:{black_count}, white:{white_count}')
        valid_clusters.append(cluster_id)
    else:
      continue

  # 시각화
  # visualize_dbscan(features, valid_clusters, dbscan_labels)

  return_array = []

  # 각 군집에 대한 최소/최대 x, y값 계산
  for label in valid_clusters:
    if label == -1:
      # 노이즈로 분류된 외곽선은 무시
      continue
      
    # 해당 군집의 외곽선 선택
    class_member_mask = (dbscan_labels == label)
    cluster_points = features[class_member_mask]
      
    # 최소 x, 최대 x, 최소 y, 최대 y값 계산
    min_x = np.min(cluster_points[:, 0])
    max_x = np.max(cluster_points[:, 0])
    min_y = np.min(cluster_points[:, 1])
    max_y = np.max(cluster_points[:, 1])
    width = max_x-min_x
    height = max_y-min_y
    
    if min_x < 150 or max_x > 1800:
      # print(f'min_x:{min_x}, max_x:{max_x}')
      # print(f'min_y:{min_y}, max_y:{max_y}')
      # print(f'x: {max_x-min_x} y: {max_y-min_y}')
      if ((width>150 and height>175) and (width<400 and height<300)):
        cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 255), 2)
        return_array.append([min_x, min_y, max_x, max_y])
      else:
        cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (255, 255, 255), 2)
      # go = not True
      # if go:
      #   roi = mask[min_y:min_y+height, min_x:min_x+width]
      #   # OCR을 통해 텍스트 추출 (Tesseract OCR 사용)
      #   text = pytesseract.image_to_string(roi, config=config)  # psm 6은 단일 블록 텍스트 감지
      #   # 추출된 텍스트 출력
      #   if text.strip():
      #     print(f"Detected text{width, height}: {text.strip()}")
      #     # 군집 경계 상자를 원본 이미지에 그리기
      #     cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 0), 3)
      #   else:
      #     cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 255), 3)
    else:
      cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)
  return return_array

def cluster_contour_by_center(contours, eps):
  """
  채팅창으로 추정되는 윤곽들의 군집도가 가장 높은 곳의 

  Args:
    contours (array): 윤곽들 좌표 배열.
    eps (integer): dbscan 데이터 거리

  Returns:
    integer: 성공하면 평균 면적과 중심점, 실패하면 False
  """
  # 중심점 구하기
  centers = []
  for contour in contours:
    min_x, min_y, max_x, max_y = contour
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    centers.append([center_x, center_y])
  centers = np.array(centers)

  # DBSCAN 클러스터링
  count = 10
  while(True):
    dbscan = DBSCAN(eps=eps, min_samples=2)
    labels = dbscan.fit_predict(centers)
    check_result = check_labels(labels)
    if check_result == 0 :
      for label in set(labels):
        if label == -1:
          continue
        mask = (labels == label)
        true_contours = [contours[i] for i in range(len(mask)) if mask[i]]
        true_centers = [centers[i] for i in range(len(mask)) if mask[i]]
        contours_average = average_contour_coordinates(true_contours)
        centers_average = average_centers(true_centers)
        
        return contours_average, centers_average
    elif check_result == 1:
      eps = eps - 5
    elif check_result == 2:
      eps = eps + 5

    if count == 0:
      print('생각하기 싫다')
      return False
    
    count = count - 1