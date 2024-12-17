import cv2

def get_total_frames_and_cap(video_path):
  cap = cv2.VideoCapture(video_path)
  if not cap.isOpened():
    print('video is not opened')
    return 0
  total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  return total_frames - 500, cap

def get_roof_images_as_array(cap, roof_frame):
  images = []
  frames_array = [roof_frame + 100 * i for i in range(5)]
  for i in frames_array:
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()
    if not ret:
      print(f"프레임 {i}을(를) 읽을 수 없습니다.")
      break
    images.append(frame)

  return images

def get_all_images_as_array(video_path):
  cap = cv2.VideoCapture(video_path)

  if not cap.isOpened():
    print('video is not opened')
    return None
  
  total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  ten_frames = int(total_frames / 10)
  result_array = [ten_frames * i for i in range(1, 11)]

  images = []
  for i in result_array:
    print(i)
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()
    if not ret:
      print(f"프레임 {i}을(를) 읽을 수 없습니다.")
      break
    images.append(frame)

  cap.release()
  return images


def get_images_as_array(video_path, fps, start_frame, interval):
  cap = cv2.VideoCapture(video_path)

  if not cap.isOpened():
    print("비디오 파일을 열 수 없습니다.")
    return None
  
  total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  print(f'total_frames: {total_frames}')

  if start_frame >= total_frames:
    print("유효하지 않은 프레임 범위입니다.")
    cap.release()
    return None
  
  #cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
  images = []
  for i in range(start_frame, start_frame+fps*interval, fps):
    print(i)
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = cap.read()
    if not ret:
      print(f"프레임 {i}을(를) 읽을 수 없습니다.")
      break
    images.append(frame)

  cap.release()
  return images

def asdf(cap):
  target_frame, total_frames = 1
  if target_frame < total_frames:
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
    ret, frame = cap.read()

    if ret:
      # 프레임을 출력
      cv2.imshow('Frame 3004', frame)
      cv2.waitKey(0)  # 아무 키나 누르면 창 닫힘
    else:
      print("프레임을 읽을 수 없습니다.")
  else:
    print("지정한 프레임이 총 프레임 수를 초과했습니다.")

  cap.release()
  cv2.destroyAllWindows()