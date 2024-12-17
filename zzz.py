import cv2
import pytesseract
import numpy as np

# 이미지에서 하얀색 텍스트를 감지하고 OCR을 적용하는 함수

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_white_text_and_ocr(image_path):
    # 이미지 불러오기
    image = cv2.imread(image_path)

    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 하얀색 텍스트만을 감지하기 위해 이진화(Thresholding) 적용
    # 하얀색의 범위를 지정 (200~255 사이의 밝은 값)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # 컨투어(외곽선) 탐지
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 자막으로 추정되는 영역에 OCR 적용
    for contour in contours:
        # 컨투어의 경계 상자를 구하기 (bounding box)
        x, y, w, h = cv2.boundingRect(contour)

        # 자막의 크기를 추정하기 위해 특정 크기 이상의 박스만 선택
        if w > 50 and h > 15:  # 텍스트로 추정되는 크기의 필터링
            # 해당 영역을 잘라내기
            roi = image[y:y+h, x:x+w]

            # OCR을 통해 텍스트 추출 (Tesseract OCR 사용)
            text = pytesseract.image_to_string(roi, config='--psm 6')  # psm 6은 단일 블록 텍스트 감지

            # 추출된 텍스트 출력
            if text.strip():
                print(f"Detected text: {text.strip()}")
                # OCR로 인식한 영역을 시각화 (필요시)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # 결과 이미지를 보여줌
    cv2.imshow('Detected Text', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 예시 이미지 경로
image_path = 'nok.png'  # 추출한 영상 프레임 경로를 넣으세요
detect_white_text_and_ocr(image_path)
