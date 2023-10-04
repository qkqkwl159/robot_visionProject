import sys
import numpy as np
import cv2

# 관심영역을 모서리 네개로 선택하는 함수
def drawROI(img, corners): # corners는 아래의 scrQuad 좌표
    cpy = img.copy() # 전송받은 이미지의 복사본을 만들어서 그 위에 그림을 그린다

    c1 = (192, 192, 255) # 모서리 색상 BGR
    c2 = (128, 128, 255) # 선 색상 BGR

    # 모서리 수 만큼 원 생성, corners 정보 이용
    for pt in corners: 
        print(pt)
        cv2.circle(cpy, (int(pt[0]), int(pt[1])), 25, c1, -1, cv2.LINE_AA)

    # 모서리를 잇는 선, 점들의 좌표는 튜플
    cv2.line(cpy, (int(corners[0][0]), int(corners[0][1])), (int(corners[1][0]), int(corners[1][1])), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, (int(corners[1][0]), int(corners[1][1])), (int(corners[2][0]), int(corners[2][1])), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, (int(corners[2][0]), int(corners[2][1])), (int(corners[3][0]), int(corners[3][1])), c2, 2, cv2.LINE_AA)
    cv2.line(cpy, (int(corners[3][0]), int(corners[3][1])), (int(corners[0][0]), int(corners[0][1])), c2, 2, cv2.LINE_AA)

    # addWeighted를 이용해서 입력 영상과 cpy영상에 가중치를 적용하여 투명도 적용
    disp = cv2.addWeighted(img, 0.3, cpy, 0.7, 0) # 모서리와 선 밑에 있는 글씨도 보임. 하지만 연산이 오래 걸린다

    return disp

def onMouse(event, x, y, flags, param): # 외관상 5개 인자. flags는 키가 눌린 여부, param은 전송 데이터
    global srcQuad, dragSrc, ptOld, src # 전역 변수 갖고 옴

    # 왼쪽 마우스가 눌렸을 때
    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(4):
            if cv2.norm(srcQuad[i] - (x,y)) < 25: # 클릭한 점이 원 안에 있는지 확인
                dragSrc[i] = True
                ptOld = (x,y) # 마우스를 이동할때 모서리도 따라 움직이도록 설정
                break
    # 마우스를 땠다면
    if event == cv2.EVENT_LBUTTONUP:
        for i in range(4):
            dragSrc[i] = False
    
    # 마우스 왼쪽 버튼이 눌려 있을 때 모서리 움직임
    if event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):
            if dragSrc[i]: # dragSrc가 True일 때
                dx = x - ptOld[0] # 이전의 마우스 점에서 dx, dy만큼 이동
                dy = y - ptOld[1]

                srcQuad[i] += (dx, dy) # 이동한 만큼 더해줌

                cpy = drawROI(src, srcQuad)
                cv2.imshow('img', cpy) # 수정된 좌표로 모서리 이동
                ptOld = (x,y) # 현재 점으로 설정
                break

            
            
            
            
# 입력 이미지 불러오기
src = cv2.imread('/Users/gimhuijun/Library/Mobile Documents/com~apple~CloudDocs/대학수업/2023_4_2/로봇비전/robot_visionProject/IMG_6598.jpg')

if src is None:
    print('Image open failed!')
    sys.exit()

# 입력 영상 크기 및 출력 영상 크기
h, w = src.shape[:2]
dw = 500 # 똑바로 핀 영상의 가로 크기
dh = round(dw*297 / 210) # A4 용지 크기: 210x297cm 이용


# 모서리 점들의 좌표, 드래그 상태 여부
# 내가 선택하려는 모서리 점 4개를 저장하는 넘파이 행렬, 30은 임의로 초기점의 좌표를 설정
# 완전히 구석이 아니라 모서리를 클릭할 수 있도록 자리를 둠
srcQuad = np.array([[100, 100], [100, h-100], [w-100, h-100], [w-100, 100]], np.float32) # 모서리 위치

# 반시계 방향으로 출력 방향의 위치
dstQuad = np.array([[0, 0], [0, dh-1], [dw-1, dh-1], [dw-1, 0]], np.float32)

# 4개의 점 중에서 현재 어떤 점을 드래고 하고 있나 상태를 저장, 점을 선택하면 True, 떼면 False
dragSrc = [False, False, False, False]


# 모서리점, 사각형 그리기
# src에 srcQuad좌표를 전송해서 화면에 나타냄
disp = drawROI(src, srcQuad)

cv2.imshow('img', disp)
cv2.setMouseCallback('img', onMouse)

while True:
    key = cv2.waitKey()
    if key == 13: # Enter 키; 엔터키 누르면 투시 변환과 결과 영상 출력
        break
    elif key == 27: # ESC 키; 종료
        cv2.destroyWindow('img')
        sys.exit()



# 투시 변환
pers = cv2.getPerspectiveTransform(srcQuad, dstQuad) # 3X3 투시 변환 행렬 생성
dst = cv2.warpPerspective(src, pers, (dw, dh), flags=cv2.INTER_CUBIC) # 가로 세로 크기는 자동
#Create sharpening filter

kernel_sharpening = np.array([[-1, -1, -1],
                              [-1,9,-1],
                             [-1,-1,-1]])

dst = cv2.filter2D(src, -1 , kernel_sharpening)# 
# 결과 영상 출력
cv2.imshow('dst', dst)

while True:
    if cv2.waitKey() == 27:
        break

cv2.destroyAllWindows()