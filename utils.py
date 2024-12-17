import numpy as np

def check_labels(labels):
  """
  DBSCAN 라벨이 적절히 분류되었는지 확인.
  """
  has_noise = -1 in labels
  label_count = len(set(labels))

  if has_noise:
    if label_count == 1:
      return 2  # 쓰레기 하나뿐
    elif label_count == 2:
      return 0  # 쓰레기와 클린 군집 존재
    else:  # label_count > 2
      return 1  # 군집이 통일되지 않음
  else:
    if label_count == 1:
      return 0
    else:
      return 1  # 단일 군집인지 확인

# def adjust_eps(target_function, start_eps=50, min_eps=1, max_eps=50, max_iterations=10):
#   """
#   eps 값을 조정하는 알고리즘.
#   """
#   eps = start_eps
#   prev_eps = None
#   iteration = 0
#   decrease_factor = 1.0  # 감소량을 제어하는 초기 값

#   while iteration < max_iterations:
#     if target_function(eps):
#       return eps  # 원하는 결과를 얻으면 종료

#     # eps 조정
#     if prev_eps is None or eps < prev_eps:  # 감소하거나 처음 반복일 때
#       prev_eps = eps
#       eps = max(eps - decrease_factor, min_eps)  # eps를 줄임
#       decrease_factor /= 1.5  # 점진적으로 감소폭 줄이기
#     else:  # 결과가 악화되면 eps를 증가
#       eps = min(eps + decrease_factor, max_eps)  # 이전 값을 초과하지 않도록 제한
#       decrease_factor *= 1.2  # 복구 시 증가폭 확대
#     iteration += 1
#   return eps  # 최대 반복 시 현재 eps 반환
def average_contour_coordinates(contours):
  """
  사각형 좌표들의 평균을 계산하는 함수.
  """

  total_min_x = total_min_y = total_max_x = total_max_y = 0
  count = len(contours)

  for rect in contours:
    # np.int32를 일반 int 타입으로 변환
    min_x, min_y, max_x, max_y = map(int, rect)
    total_min_x += min_x
    total_min_y += min_y
    total_max_x += max_x
    total_max_y += max_y

  avg_min_x = total_min_x / count
  avg_min_y = total_min_y / count
  avg_max_x = total_max_x / count
  avg_max_y = total_max_y / count

  return [avg_min_x, avg_min_y, avg_max_x, avg_max_y]

def average_centers(centers):
    """
    주어진 좌표 리스트의 평균을 계산하는 함수
    """
    # 리스트를 NumPy 배열로 변환
    coordinates_array = np.array(centers)
    # x, y의 평균 계산
    mean_coordinates = np.mean(coordinates_array, axis=0)
    
    return mean_coordinates

def get_time_to_frame(fps, y, m, s):
  frame = fps*(y*3600+m*60+s)
  return frame

if __name__ == '__main__':

  #5:14:58~5:14:59
  frame = get_time_to_frame(60, 0, 7, 23)
  print(frame)

  fps = 30
  start = 1
  interval = 3

  for i in range(start, fps*interval, fps):
    print(i)