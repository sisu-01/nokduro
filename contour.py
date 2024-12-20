import cv2
import numpy as np
import math

# 색상 범위 설정
COLOR_RANGES = {
  'white': (np.array([254, 244, 254]), np.array([255, 255, 255])),
  'black': (np.array([0, 0, 0]), np.array([0, 0, 0]))
}
# 최소 면적 기준
MIN_AREA = 55
#컨투어 최소 길이
CONTOUR_MIN_LENGTH = {
  'white': 0,
  'black': 0
}

def unnamed(image):
  white_features, w_mask = get_individual_contours_features_as_array(image, 'white')
  black_features, b_mask = get_individual_contours_features_as_array(image, 'black')
  combined_features = np.vstack((white_features, black_features))
  colors = ['white'] * len(white_features) + ['black'] * len(black_features)
  return combined_features, colors

def get_individual_contours_features_as_array(image, color):
  lower_rgb, upper_rgb = COLOR_RANGES[color]
  mask = cv2.inRange(image, lower_rgb, upper_rgb)
  contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  features = []
  for contour in contours:
    M = cv2.moments(contour)
    if M['m00'] < MIN_AREA:
      length = cv2.arcLength(contour, closed=False)
      #CONTOUR_MIN_LENGTH는 특정 색이 넘어야되는 최소길이
      if CONTOUR_MIN_LENGTH[color] < length < 5:
        x, y = contour[0][0]
        features.append([x, y])
        if color == 'white':
          cv2.rectangle(image, (x, y), (x + 2, y + 2), (255, 0, 0), 2)#파랑 중심점
        else:
          cv2.rectangle(image, (x, y), (x + 2, y + 2), (0, 0, 255), 2)#빨강 중심점
      else:
        # 컨투어 포인트가 1개뿐인 경우 -1px-
        if len(contour) == 1:
          x, y = contour[0][0]
          if color == 'white':
            features.append([x, y])
            cv2.rectangle(image, (x, y), (x + 2, y + 2), (255, 0, 0), 2)#파랑 중심점
          else:
            cv2.rectangle(image, (x, y), (x + 2, y + 2), (0, 0, 255), 2)#빨강 중심점
        # 이새기들은 뭘까
        else:
          x, y = contour[0][0]
          if color == 'white':
            features.append([x, y])
            cv2.rectangle(image, (x, y), (x + 2, y + 2), (255, 0, 0), 2)#파랑 중심점
          else:
            cv2.rectangle(image, (x, y), (x + 2, y + 2), (0, 0, 255), 2)#빨강 중심점
  return np.array(features), mask

def compare_prev_and_present(prev, present):
  # Unpack the previous and present values
  prev_contour, prev_center = prev
  present_contour, present_center = present

  # Calculate the difference in centers
  center_distance = math.sqrt((prev_center[0] - present_center[0]) ** 2 + (prev_center[1] - present_center[1]) ** 2)
  # Check if the center is within 50 pixels
  is_center_close = center_distance < 50

  # Calculate the sizes of the rectangles
  prev_width = prev_contour[2] - prev_contour[0]
  prev_height = prev_contour[3] - prev_contour[1]
  present_width = present_contour[2] - present_contour[0]
  present_height = present_contour[3] - present_contour[1]

  # Check if the sizes are within 50 pixels difference
  is_size_similar = abs(prev_width - present_width) < 60 and abs(prev_height - present_height) < 60

  # Return True if both conditions are met
  return is_center_close and is_size_similar

if __name__ == '__main__':
  prev_contour = [1547.25, 409.5, 1887.75, 624.75]
  prev_center = [1717.5, 517.125]
  contour = [12.333333333333334, 543.6666666666666, 338.6666666666667, 737.0]
  center = [170.375, 638.25]
  a = compare_prev_and_present([prev_contour, prev_center], [contour, center])

# def get_contours_features_as_array(image, color, other_features=[]):
#   lower, upper = COLOR_RANGES[color]
#   mask = cv2.inRange(image, lower, upper)
#   contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) #CHAIN_APPROX_SIMPLE

#   features = other_features.copy()
#   for contour in contours:
#     M = cv2.moments(contour)
#     if M["m00"] >= MIN_AREA:
#       cx = int(M["m10"] / M["m00"])
#       cy = int(M["m01"] / M["m00"])
#       #features.append([cx, cy])
#       cv2.rectangle(image, (cx, cy), (cx + 2, cy + 2), (10, 10, 10), 5)#검정 중심점
#     # 면적이 없고 길이가 있는 컨투어에 대해 길이 계산
#     else:
#       length = cv2.arcLength(contour, closed=False)
#       if CONTOUR_MIN_LENGTH[color] < length and length < 5:
#         # 컨투어의 좌표로부터 첫 번째 점을 사용하여 사각형 그리기
#         x, y = contour[0][0]
#         features.append([x, y])
#         cv2.rectangle(image, (x, y), (x + 2, y + 2), (255, 0, 0), 2)#파랑 중심점
#       else:
#         if len(contour) == 1:  # 컨투어 포인트가 1개뿐인 경우 -1px-
#           x, y = contour[0][0]
#           if color == 'white':
#             features.append([x, y])
#             cv2.rectangle(image, (x, y), (x + 2, y + 2), (0, 255, 0), 2)#초록 중심점
#         else:
#           x, y = contour[0][0]
#           if color == 'white':
#             features.append([x, y])
#             cv2.rectangle(image, (x, y), (x + 2, y + 2), (0, 0, 255), 2)#빨강 중심점
#   #return np.array(features), mask
#   if any(other_features):
#     return np.array(features), mask
#   else:
#     return features, mask