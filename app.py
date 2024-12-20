import cv2
from clustering import cluster_contour_features, cluster_contour_by_center
from contour import unnamed, compare_prev_and_present
from video_utils import get_total_frames_and_cap, get_roof_images_as_array
import numpy as np

video_path = 'video/video.webm'
EPS = 35
run = True

total_frame, cap = get_total_frames_and_cap(video_path)
if total_frame < 0:
  run = False
per_number = 10
ten_total_frame = int(total_frame / per_number)
roof_count = per_number - 1

prev_contour = []
prev_center = []

print(f'total_frame: {total_frame}')
while(run):
  print(f'roof_count: {roof_count}')
  roof_frame = ten_total_frame * (roof_count+1)
  images = get_roof_images_as_array(cap, roof_frame)
  if images is not None:
    images_contours = []
    for idx, image in enumerate(images):
      features, colors = unnamed(image)
      single_image_contour = cluster_contour_features(features, colors, image, EPS=EPS)
      if single_image_contour:
        images_contours = images_contours+single_image_contour

      if 10 == 101:
        cv2.imshow(f'image {idx}', image)
        #cv2.imshow(f'w_mask {start_frame}', b_mask)
        if cv2.waitKey(0) & 0xFF == ord('q'):
          break  # 'q' 키를 누르면 중지
        cv2.destroyAllWindows()
    # end for
    contour, center = cluster_contour_by_center(images_contours, 50)

    if np.any(prev_contour) and np.any(prev_center):
      prev = [prev_contour, prev_center]
      present = [contour, center]
      is_same_place = compare_prev_and_present(prev, present)
      if not is_same_place:
        print('위치가 변경되었다!@##!@#@!#@')
        
    else:
      print('최초니까 일단은 넘어갑니다')
    
    prev_contour = contour
    prev_center = center
  # end if  
  roof_count = roof_count - 1
  if roof_count < 1:
    break
  else:
    if roof_count == 6:
      break
# end while




#fps = 60
#start_frame = 0
#start_frame = 123523
#interval = 1
# if start_frame == 0:
#   import random
#   start_frame = random.randrange(1, 1293314)
#비디오에서 이미지 목록을 배열로 가져와버려
#images = get_images_as_array(video_path, fps, start_frame, interval)
#images = get_all_images_as_array(video_path)
# if images is not None:
#   for idx, image in enumerate(images):
#     white_features, w_mask = get_individual_contours_features_as_array(image, 'white')
#     black_features, b_mask = get_individual_contours_features_as_array(image, 'black')
#     combined_features = np.vstack((white_features, black_features))
#     colors = ['white'] * len(white_features) + ['black'] * len(black_features)
#     array = cluster_contour_features(combined_features, colors, image, EPS=EPS)
#     print(len(array))

#     cv2.imshow(f'image {idx}', image)
#     #cv2.imshow(f'w_mask {start_frame}', b_mask)

#     # 500ms 동안 이미지 표시 (값을 조정하여 속도 변경 가능)
#     if cv2.waitKey(0) & 0xFF == ord('q'):
#       break  # 'q' 키를 누르면 중지
#   cv2.destroyAllWindows()
# else:
#   print("이미지를 가져오지 못했습니다.")

#글씨크기, 채팅창 위치, 채팅창 크기