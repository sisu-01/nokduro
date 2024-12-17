#import pytesseract
import cv2
import numpy as np
from sklearn.cluster import DBSCAN

#환경변수
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# 설정
#config = ('-l kor+eng --oem 3 --psm 11')#config = ('--psm 6')

threshold = 240 # 임계값
lower_white = np.array([244, 234, 244])  # 최소 흰색 값
upper_white = np.array([255, 255, 255])  # 최대 흰색 값
area = 15 #면적
eps = 75 #dbscan 거리

def test(image):
    mask = cv2.inRange(image, lower_white, upper_white)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    features = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] >= area:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            #features.append([cx, cy])
            #빨강 중심점
            cv2.rectangle(image, (cx, cy), (cx + 2, cy + 2), (0, 0, 255), 2)
        # 면적이 없고 길이가 있는 컨투어에 대해 길이 계산
        else:
            length = cv2.arcLength(contour, closed=False)
            if 0 < length and length < 5:  # 길이가 5 이상인 경우에만
                # 컨투어의 좌표로부터 첫 번째 점을 사용하여 사각형 그리기
                x, y = contour[0][0]
                features.append([x, y])
                #파랑 중심점
                cv2.rectangle(image, (x, y), (x + 2, y + 2), (255, 0, 0), 2)
            else:
                # 1px 크기인 경우
                if len(contour) == 1:  # 컨투어 포인트가 1개뿐인 경우
                    x, y = contour[0][0]
                    features.append([x, y])
                    cv2.rectangle(image, (x, y), (x + 2, y + 2), (0, 255, 0), 2)  # 초록색 사각형
                else:
                    cv2.rectangle(image, (x, y), (x + 2, y + 2), (0, 255, 0), 2)  # 초록색 사각형

    return image, mask
    # DBSCAN 클러스터링 적용
    features = np.array(features)
    dbscan = DBSCAN(eps=eps, min_samples=5)  # eps와 min_samples는 데이터에 따라 조정
    labels = dbscan.fit_predict(features)

    # 각 군집에 대한 최소/최대 x, y값 계산
    unique_labels = set(labels)
    for label in unique_labels:
        if label == -1:
            # 노이즈로 분류된 외곽선은 무시
            continue
        
        # 해당 군집의 외곽선 선택
        class_member_mask = (labels == label)
        cluster_points = features[class_member_mask]
        
        # 최소 x, 최대 x, 최소 y, 최대 y값 계산
        min_x = np.min(cluster_points[:, 0])
        max_x = np.max(cluster_points[:, 0])
        min_y = np.min(cluster_points[:, 1])
        max_y = np.max(cluster_points[:, 1])
        width = max_x-min_x
        height = max_y-min_y
        
        if width > 100 / 2 and height > 25 / 2:
            cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
            go = not True
            if go:
                roi = mask[min_y:min_y+height, min_x:min_x+width]
                # OCR을 통해 텍스트 추출 (Tesseract OCR 사용)
                text = pytesseract.image_to_string(roi, config=config)  # psm 6은 단일 블록 텍스트 감지
                # 추출된 텍스트 출력
                if text.strip():
                    print(f"Detected text{width, height}: {text.strip()}")
                    # 군집 경계 상자를 원본 이미지에 그리기
                    cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 0), 3)
                else:
                    cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 255), 3)
    return image, mask

# def thres(image_path, way):
#     if way == 0:
#         image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#         ret, th1 = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
#         return image, th1
#     elif way == 1:
#         image = cv2.imread(image_path)
#         mask = cv2.inRange(image, lower_white, upper_white)
#         return image, mask

# def detect_white_cluster(image_path):

#     image, converted = thres(image_path, 1)
#     # 컨투어(외곽선) 탐지
#     contours, _ = cv2.findContours(converted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # 외곽선의 중심 좌표를 계산하고 저장
#     features = []
#     for contour in contours:
#         M = cv2.moments(contour)
#         if M["m00"] >= 10:
#             cx = int(M["m10"] / M["m00"])
#             cy = int(M["m01"] / M["m00"])
#             features.append([cx, cy])
#             #빨강 중심점
#             cv2.rectangle(image, (cx, cy), (cx + 5, cy + 5), (0, 0, 255), 10)
        

#     # DBSCAN 클러스터링 적용
#     features = np.array(features)
#     dbscan = DBSCAN(eps=eps, min_samples=2)  # eps와 min_samples는 데이터에 따라 조정
#     labels = dbscan.fit_predict(features)

#     # 각 군집에 대한 최소/최대 x, y값 계산
#     unique_labels = set(labels)
#     for label in unique_labels:
#         if label == -1:
#             # 노이즈로 분류된 외곽선은 무시
#             continue
        
#         # 해당 군집의 외곽선 선택
#         class_member_mask = (labels == label)
#         cluster_points = features[class_member_mask]
        
#         # 최소 x, 최대 x, 최소 y, 최대 y값 계산
#         min_x = np.min(cluster_points[:, 0])
#         max_x = np.max(cluster_points[:, 0])
#         min_y = np.min(cluster_points[:, 1])
#         max_y = np.max(cluster_points[:, 1])
#         width = max_x-min_x
#         height = max_y-min_y
        
#         if width > 100 and height > 25:
#             cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 0), 1)
#             go = not True
#             if go:
#                 roi = converted[min_y:min_y+height, min_x:min_x+width]
#                 # OCR을 통해 텍스트 추출 (Tesseract OCR 사용)
#                 text = pytesseract.image_to_string(roi, config=config)  # psm 6은 단일 블록 텍스트 감지
#                 # 추출된 텍스트 출력
#                 if text.strip():
#                     print(f"Detected text{width, height}: {text.strip()}")
#                     # 군집 경계 상자를 원본 이미지에 그리기
#                     cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 0), 3)
#                 else:
#                     cv2.rectangle(image, (min_x, min_y), (max_x, max_y), (0, 255, 255), 3)

#     # 결과 시각화
#     cv2.imshow('Clustered Contours', image)
#     cv2.imshow('Converted Image', converted)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


if __name__ == "__main__":
    # 예시 이미지 경로
    image_path = 'nok5.png'  # 추출한 영상 프레임 경로를 넣으세요
    print('zz')
    #detect_white_cluster(image_path)