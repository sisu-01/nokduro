import cv2
from clustering import cluster_contour_features, cluster_contour_by_center
from contour import unnamed
from video_utils import get_total_frames_and_cap, get_roof_images_as_array

video_path = 'video/video.webm'
EPS = 35
run = True

total_frame, cap = get_total_frames_and_cap(video_path)
if total_frame < 0:
  run = False
per_number = 10
ten_total_frame = int(total_frame / per_number)
roof_count = per_number - 6

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

      if 10 == 10:
        cv2.imshow(f'image {idx}', image)
        #cv2.imshow(f'w_mask {start_frame}', b_mask)
        if cv2.waitKey(0) & 0xFF == ord('q'):
          break  # 'q' 키를 누르면 중지
        cv2.destroyAllWindows()
    # end for
    contour, center = cluster_contour_by_center(images_contours, 50)
    print(contour, center)
    #total_intersection_area(images_contours)
    
  roof_count = roof_count - 1
  if roof_count < 1:
    break
  else:
    break





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