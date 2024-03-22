import math
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter.simpledialog import *
import os.path
### 함수부
#*************************
# 공통 함수부
#*************************
def malloc2D(h, w, initValue = 0) :
    memory = [ [initValue for _ in range(w)] for _ in range(h)]
    return memory
def openImage():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    fullname = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')))
    # 입력 이미지 크기를 결정
    fsize = os.path.getsize(fullname)
    inH = inW = int(math.sqrt(fsize))
    # 메모리 확보
    inImage = malloc2D(inH, inW)
    # 파일 --> 메모리
    rfp = open(fullname, 'rb')
    for i in range(inH):
        for k in range(inW):
            inImage[i][k] = ord(rfp.read(1))
    rfp.close()
    equalImage()
def opencircleImage():
    global window, canvas, paper, fullname
    global inImage, outImage, circleImage, inH, inW, outH, outW
    fullname = askopenfilename(parent=window, filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*')))
    # 입력 이미지 크기를 결정
    fsize = os.path.getsize(fullname)
    cirH = cirW = int(math.sqrt(fsize))
    # 입력 이미지와 크기가 같아야 실행
    if (inH != cirH) & (inW != cirW):
        print("이미지 크기가 다릅니다.\n")
        return
    # 메모리 확보
    circleImage = malloc2D(cirH, cirW)
    # 파일 --> 메모리
    cfp = open(fullname, 'rb')
    for i in range(inH):
        for k in range(inW):
            circleImage[i][k] = ord(cfp.read(1))
    cfp.close()
def saveImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    if (outImage == None) | (len(outImage) == 0) :
        return
    wfp = asksaveasfile(parent=window, mode='wb', defaultextension='*.raw',
                        filetypes=(('RAW파일', '*.raw'), ('모든파일', '*.*'))  )
    import struct
    for i in range(outH) :
        for k in range(outW) :
            wfp.write( struct.pack('B', outImage[i][k]) )
    wfp.close()
    messagebox.showinfo('성공', wfp.name + ' 저장 완료')
def displayImage() :
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    ## 기존에 이미지를 오픈한적이 있으면, 캔버스 뜯어내기
    if (canvas != None) :
        canvas.destroy()
    ## 벽, 캔버스, 종이 설정
    window.geometry(str(outH)+'x'+str(outW)) # "512x512"
    canvas = Canvas(window, height=outH, width=outW, bg='yellow')  # 칠판
    paper = PhotoImage(height=outH, width=outW)  # 종이
    canvas.create_image((outH // 2, outW // 2), image=paper, state='normal')
    ## 메모리 --> 화면
    # for i in range(inH):
    #     for k in range(inW):
    #         r = g = b = inImage[i][k]
    #         paper.put('#%02x%02x%02x' % (r, g, b), (k, i))
    # 더블 버퍼링... 비슷한 기법 (모두다 메모리상에 출력형태로 생성한 후에, 한방에 출력)
    rgbString = "" # 전체에 대한 16진수 문자열
    for i in range(outH) :
        oneString = "" # 한줄에 대한 16진수 문자열
        for k in range(outW) :
            r = g = b = outImage[i][k]
            oneString += '#%02x%02x%02x ' % (r, g, b)
        rgbString += '{' + oneString + '} '
    paper.put(rgbString)
    canvas.pack()

#*************************
# 영상처리 함수부
#*************************
def equalImage():
    global window, canvas, paper, fullname
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]
    ########################################
    displayImage()

def addImage(): ## 밝기 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    Value = askinteger("정수입력 : ", '-255 ~ 255 입력', maxvalue = 255, minvalue = -255)
    for i in range(inH):
        for k in range(inW):
            px = inImage[i][k] + Value
            if (px > 255):
                px = 255
            elif (px < 0):
                px = 0
            outImage[i][k] = px
    ########################################
    displayImage()

def reverseImage(): ## 반전 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255 - inImage[i][k]
    ########################################
    displayImage()

def bwImage(): ## 흑백 (127) 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] > 127:
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    ########################################
    displayImage()

def bwAvgImage():  ## 흑백 알고리즘 (평균값)
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 평균값 계산
    hap = 0
    for i in range(0, inH, 1):
        for k in range(0, inW, 1):
            hap += inImage[i][k]
    avg = hap / (outW * outH)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] > avg:
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    ########################################
    displayImage()

def bwMedImage():  ## 흑백 알고리즘 (중앙값)
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    aryImage = []
    for i in range(inH):
        for k in range(inW):
            aryImage.append(inImage[i][k])
    aryImage.sort()
    mid = aryImage[len(aryImage) // 2]
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] > mid:
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    ########################################
    displayImage()

def gammaImage(): ## 감마 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    gamma = askfloat("실수입력 : ", '0.2 ~ 1.8 입력', maxvalue = 1.8, minvalue = 0.2)
    for i in range(inH):
        for k in range(inW):
            m = float(inImage[i][k])
            outImage[i][k] = int((255.0 * pow((m / 255.0), gamma)))
    ########################################
    displayImage()

def paraCapImage():  ## 파라볼라 CAP 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            m = float(inImage[i][k])
            outImage[i][k] = int(255.0 - 255.0 * pow((m / 128.0 - 1.0), 2))
    ########################################
    displayImage()

def paraCupImage():  ## 파라볼라 CUP 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            m = float(inImage[i][k])
            outImage[i][k] = int(255.0 * pow((m / 128.0 - 1.0), 2))
    ########################################
    displayImage()

def andImage():  ## AND 알고리즘
    global window, canvas, paper
    global inImage, outImage, circleImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    opencircleImage()
    # 원형 이미지를 못 받아오면 취소
    if(circleImage == None):
        return
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] & circleImage[i][k]
    ########################################
    displayImage()

def orImage():  ## OR 알고리즘
    global window, canvas, paper
    global inImage, outImage, circleImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    opencircleImage()
    # 원형 이미지를 못 받아오면 취소
    if (circleImage == None):
        return
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] | circleImage[i][k]
    ########################################
    displayImage()

def xorImage():  ## XOR 알고리즘
    global window, canvas, paper
    global inImage, outImage, circleImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    opencircleImage()
    # 원형 이미지를 못 받아오면 취소
    if (circleImage == None):
        return
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] ^ circleImage[i][k]
    ########################################
    displayImage()

def zoomOutImage():  ## 축소 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    scale = askinteger("정수입력 : ", '0 ~ 100 입력', maxvalue = 100, minvalue = 0)
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH // scale
    outW = inW // scale
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i // scale][k // scale] = inImage[i][k]
    ########################################
    displayImage()


def zoomOutAvgImage():  ## 축소(평균값) 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    scale = askinteger("정수입력 : ", '0 ~ 100 입력', maxvalue = 100, minvalue = 0)
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH // scale
    outW = inW // scale
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            hap = 0
            cnt = 0
            for n in range(-1, 2, 1):
                for m in range(-1, 2, 1):
                    if (0 <= i + n) & (i + n < inH) & (0 <= k + m) & (k + m < inW):
                        hap += int(inImage[i + n][k + m])
                        cnt += 1
            Value = hap // cnt
            outImage[i // scale][k // scale] = Value
    ########################################
    displayImage()


def zoomOutMedImage():  ## 축소(중앙값) 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    scale = askinteger("정수입력 : ", '0 ~ 100 입력', maxvalue=100, minvalue=0)
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH // scale
    outW = inW // scale
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            aryImage = []
            cnt = 0
            for n in range(-1, 2, 1):
                for m in range(-1, 2, 1):
                    if (0 <= i + n) & (i + n < inH) & (0 <= k + m) & (k + m < inW):
                        aryImage.append(inImage[i + n][k + m])
                        cnt += 1
            aryImage.sort()
            mid = aryImage[len(aryImage) // 2]
            outImage[i // scale][k // scale] = mid
    ########################################
    displayImage()


def zoomInImage():  ## 확대 알고리즘(포워딩)
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    scale = askinteger("정수입력 : ", '0 ~ 100 입력', maxvalue=100, minvalue=0)
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH * scale
    outW = inW * scale
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i * scale][k * scale] = inImage[i][k]
    ########################################
    displayImage()


def zoomIn2Image():  ## 확대 알고리즘(백워딩)
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    scale = askinteger("정수입력 : ", '0 ~ 100 입력', maxvalue=100, minvalue=0)
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH * scale
    outW = inW * scale
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] = inImage[i // scale][k // scale]
    ########################################
    displayImage()

def zoomInYSImage():  ## 확대 알고리즘(포워딩) + 양선형 보간
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    scale = float(askinteger("정수입력 : ", '0 ~ 100 입력', maxvalue=100, minvalue=0))
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = int(inH * scale)
    outW = int(inW * scale)
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(outH):
        for k in range(outW):
            rH = float(i / scale) # 현재 위치
            rW = float(k / scale)

            iH = math.floor(rH) # 블록의 가로세로 칸
            iW = math.floor(rW)

            sH = float(rH - iH) # 현재 블록 위치
            sW = float(rW - iW)
            if (iH < 0) | (iH >= (inH - 1)) | (iW < 0) | (iW >= (inW - 1)):
                outImage[i][k] = 255
            else:
                c1 = float(inImage[iH][iW])
                c2 = float(inImage[iH][iW + 1])
                c3 = float(inImage[iH + 1][iW + 1])
                c4 = float(inImage[iH + 1][iW])

                value = (c1 * (1 - sH) * (1 - sW)
                         + c2 * sW * (1 - sH)
                         + c3 * sW * sH
                         + c4 * (1 - sW) * sH)
                outImage[i][k] = int(value)
    ########################################
    displayImage()

def rotateImage():  ## 회전 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    # 회전 값 입력
    degree = askinteger("정수입력 : ", '0 ~ 360 입력', maxvalue=360, minvalue=0)
    radian = -(degree * 3.141592 / 180)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            xs = i
            ys = k
            xd = int(math.cos(radian) * xs - math.sin(radian) * ys)
            yd = int(math.sin(radian) * xs + math.cos(radian) * ys)
            if (0 <= xd) & (xd < outH) & (0 <= yd) & (yd < outW):
                outImage[xd][yd] = inImage[xs][ys]
    ########################################
    displayImage()

def rotate2Image():  ## 회전 알고리즘 + 중앙/백워딩
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    # 회전 값 입력
    degree = askinteger("정수입력 : ", '0 ~ 360 입력', maxvalue=360, minvalue=0)
    radian = -(degree * 3.141592 / 180)
    cx = inH // 2
    cy = inW // 2
    ### 진짜 영상처리 알고리즘 ###
    for i in range(outH):
        for k in range(outW):
            xd = i
            yd = k
            xs = int(math.cos(radian) * (xd - cx) + math.sin(radian) * (yd - cy))
            ys = int(-math.sin(radian) * (xd - cx) + math.cos(radian) * (yd - cy))
            xs += cx
            ys += cy
            if (0 <= xs) & (xs < inH) & (0 <= ys) & (ys < inW):
                outImage[xd][yd] = inImage[xs][ys]
            else:
                outImage[xd][yd] = 255
    ########################################
    displayImage()


def rotate3Image():  ## 회전 확대 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # 회전 값 입력
    degree = askinteger("정수입력 : ", '0 ~ 360 입력', maxvalue=360, minvalue=0)
    radian = -(degree * 3.141592 / 180)
    radian90 = -((90 - degree) * 3.141592 / 180)
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = int(inH * math.cos(radian90) + inW * math.cos(radian))
    outW = int(inW * math.cos(radian) + inH * math.cos(radian90))
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 입력 전 이미지 중앙 좌표
    cx = inH // 2
    cy = inW // 2
    ## 입력 후 이미지 중앙 좌표
    cx2 = outH // 2
    cy2 = outW // 2
    ### 진짜 영상처리 알고리즘 ###
    for i in range(outH):
        for k in range(outW):
            xd = i
            yd = k
            xs = int(math.cos(radian) * (xd - cx2) + math.sin(radian) * (yd - cy2))
            ys = int(-math.sin(radian) * (xd - cx2) + math.cos(radian) * (yd - cy2))
            xs += cx
            ys += cy
            if (0 <= xs) & (xs < inH) & (0 <= ys) & (ys < inW):
                outImage[xd][yd] = inImage[xs][ys]
            else:
                outImage[xd][yd] = 255
    ########################################
    displayImage()

def moveImage():  ## 이동 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    # 이동값 입력
    valueH = askinteger("정수입력 : ", '가로 값 입력')
    valueW = askinteger("정수입력 : ", '세로 값 입력')
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if (0 <= i - valueH) & (i - valueH < outH) & (0 <= k - valueW) & (k - valueW < outW):
                outImage[i][k] = inImage[i - valueH][k - valueW]
    ########################################
    displayImage()

def mirrorUDImage():  ## 상하 미러링 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[inH - i - 1][k]
    ########################################
    displayImage()

def mirrorLRImage():  ## 좌우 미러링 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][inW - k - 1]
    ########################################
    displayImage()

def histoStretchImage():  ## 히스토그렘 스트레칭 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    high = inImage[0][0]
    low = inImage[0][0]
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if (inImage[i][k] < low):
                low = inImage[i][k]
            if (inImage[i][k] > high):
                high = inImage[i][k]

    for i in range(inH):
        for k in range(inW):
            old = inImage[i][k]
            new = int((old - low) / (high - low) * 255.0)
            if (new > 255):
                new = 255
            if (new < 0):
                new = 0
            outImage[i][k] = new
    ########################################
    displayImage()

def endInImage():  ## 엔드인 탐색 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    high = inImage[0][0]
    low = inImage[0][0]
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < low:
                low = inImage[i][k]
            if inImage[i][k] > high:
                high = inImage[i][k]

    high -= 50
    low += 50

    for i in range(inH):
        for k in range(inW):
            old = inImage[i][k]
            new = int((old - low) / (high - low) * 255.0)
            if new > 255:
                new = 255
            if new < 0:
                new = 0
            outImage[i][k] = new
    ########################################
    displayImage()

def histoEqualImage():  ## 평활화 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)

    ## 1단계: 반도수 세기( = 히스토그렘)
    histo = [0 for _ in range(256)]
    for i in range(inH):
        for k in range(inW):
            histo[inImage[i][k]] += 1
    ## 2단계: 누적 히스토그렘 생성
    sumHisto = [0 for _ in range(256)]
    sumHisto[0] = histo[0]
    for i in range(256):
        sumHisto[i] = sumHisto[i - 1] + histo[i]
    ## 3 단계: 정규화된 히스토그렘 생성
    normalHisto = [0 for _ in range(256)]
    for i in range(256):
        normalHisto[i] = sumHisto[i] * (1.0 / (inH * inW) * 255.0)
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = normalHisto[inImage[i][k]]
    ########################################
    displayImage()

def embossImage():  ## 화소 영역 처리 : 엠보싱 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 화소 영역 처리
    mask = [[-1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0]]
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for n in range(0, 3, 1):
                for m in range(0, 3, 1):
                    S += tmpInImage[i + n][k + m] * mask[n][m]
            tmpOutImage[i][k] = S
    # 후처리 (마스크 값의 합계에 따라서)
    for i in range(outH):
        for k in range(outH):
            tmpOutImage[i][k] += 127.0
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

def blurImage():  ## 회소 영역 처리 : 블러링 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 화소 영역 처리
    val = askinteger("정수입력 : ", '1 ~ 9 입력', maxvalue=9, minvalue=1)
    if val == 1:
        for i in range(inH):
            for k in range(inW):
                outImage[i][k] = inImage[i][k]
        displayImage()
        return
    # 엠보싱 마스크 할당
    mask = malloc2D(val, val)
    for i in range(val):
        for k in range(val):
            mask[i][k] = 1.0 / (val * val)
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + val - 1, inW + val - 1)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + val - 1):
        for k in range(inW + val - 1):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for n in range(0, val, 1):
                for m in range(0, val, 1):
                    S += tmpInImage[i + n][k + m] * mask[n][m]
            tmpOutImage[i][k] = S
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

def SharpImage():  ## 화소 영역 처리 : 샤프닝 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 화소 영역 처리
    mask = [[0.0, -1.0, 0.0],
            [-1.0, 5.0, -1.0],
            [0.0, -1.0, 0.0]]
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for n in range(0, 3, 1):
                for m in range(0, 3, 1):
                    S += tmpInImage[i + n][k + m] * mask[n][m]
            tmpOutImage[i][k] = S
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

def gausImage():  ## 회소 영역 처리 : 가우시안 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 화소 영역 처리
    mask = [[(1.0 / 16), (1.0 / 8), (1.0 / 16)],
            [(1.0 / 8), (1.0 / 4), (1.0 / 8)],
            [(1.0 / 16), (1.0 / 8), (1.0 / 16)]]
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for n in range(0, 3, 1):
                for m in range(0, 3, 1):
                    S += tmpInImage[i + n][k + m] * mask[n][m]
            tmpOutImage[i][k] = S
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

def hpfSharpImage():  ## 회소 영역 처리 : 고주파 필터 샤프닝 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 화소 영역 처리
    mask = [[(- 1.0 / 9), (- 1.0 / 9), (- 1.0 / 9)],
            [(- 1.0 / 9), (8.0 / 9), (- 1.0 / 8)],
            [(- 1.0 / 9), (- 1.0 / 9), (- 1.0 / 9)]]
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for n in range(0, 3, 1):
                for m in range(0, 3, 1):
                    S += tmpInImage[i + n][k + m] * mask[n][m]
            tmpOutImage[i][k] = S
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

def lpfSharpImage():  ## 회소 영역 처리 : 저주파 필터 샤프닝 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 화소 영역 처리
    mask = [[(1.0 / 9), (1.0 / 9), (1.0 / 9)],
            [(1.0 / 9), (1.0 / 9), (1.0 / 8)],
            [(1.0 / 9), (1.0 / 9), (1.0 / 9)]]
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for n in range(0, 3, 1):
                for m in range(0, 3, 1):
                    S += tmpInImage[i + n][k + m] * mask[n][m]
            tmpOutImage[i][k] = inImage[i][k] - S
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

def edgeHorImage():  ## 경계선 검출 : 수평검출 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 화소 영역 처리
    mask = [[0.0, -1.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0]]
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for n in range(0, 3, 1):
                for m in range(0, 3, 1):
                    S += tmpInImage[i + n][k + m] * mask[n][m]
            tmpOutImage[i][k] = S
    # 후처리 (마스크 값의 합계에 따라서)
    for i in range(outH):
        for k in range(outH):
            tmpOutImage[i][k] += 127.0
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

def edgeVerImage():  ## 경계선 검출 : 수직검출 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 화소 영역 처리
    mask = [[0.0, 0.0, 0.0],
            [-1.0, 1.0, 0.0],
            [0.0, 0.0, 0.0]]
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for n in range(0, 3, 1):
                for m in range(0, 3, 1):
                    S += tmpInImage[i + n][k + m] * mask[n][m]
            tmpOutImage[i][k] = S
    # 후처리 (마스크 값의 합계에 따라서)
    for i in range(outH):
        for k in range(outH):
            tmpOutImage[i][k] += 127.0
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

def edgeHomogenImage():  ## 경계선 검출 : 유사 연산자 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            max = 0.0
            for n in range(0, 3, 1):
                for m in range(0, 3, 1):
                    if doubleABS(tmpInImage[i + 1][k + 1] - tmpInImage[i + n][k + m]) >= max:
                        max = doubleABS(tmpInImage[i + 1][k + 1] - tmpInImage[i + n][k + m])
            tmpOutImage[i][k] = max
    # 후처리 (마스크 값의 합계에 따라서)
    for i in range(outH):
        for k in range(outH):
            tmpOutImage[i][k] += 127.0
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

def doubleABS(X):
    if X >= 0:
        return X
    else:
        return -X

def laplacianImage(): ## 경계선 검출 : 라플라시안 처리 알고리즘
    global window, canvas, paper
    global inImage, outImage, inH, inW, outH, outW
    # (중요!) 출력 이미지  크기 결정 --> 알고리즘에 의존
    outH = inH
    outW = inW
    # 출력 이미지 메모리 확보
    outImage = malloc2D(outH, outW)
    ## 화소 영역 처리
    mask = [[0.0, 1.0, 0.0],
            [1.0, - 4.0, 1.0],
            [0.0, 1.0, 0.0]]
    # 임시 메모리 할당(실수형)
    tmpInImage = malloc2D(inH + 2, inW + 2)
    tmpOutImage = malloc2D(outH, outW)
    # 임시 입력 메모리 초기화(127) : 필요시 평균값
    for i in range(inH + 2):
        for k in range(inW + 2):
            tmpInImage[i][k] = 127
    #  입력 이미지 --> 임시 입력 이미지
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i + 1][k + 1] = inImage[i][k]
    # 회선 연산
    for i in range(inH):
        for k in range(inW):
            S = 0.0
            for n in range(0, 3, 1):
                for m in range(0, 3, 1):
                    S += tmpInImage[i + n][k + m] * mask[n][m]
            tmpOutImage[i][k] = S
    # 후처리 (마스크 값의 합계에 따라서)
    for i in range(outH):
        for k in range(outH):
            tmpOutImage[i][k] += 127.0
    ### 진짜 영상처리 알고리즘 ###
    for i in range(inH):
        for k in range(inW):
            if tmpOutImage[i][k] < 0.0:
                outImage[i][k] = 0
            elif tmpOutImage[i][k] > 255.0:
                outImage[i][k] = 255
            else:
                outImage[i][k] = int(tmpOutImage[i][k])
    ########################################
    displayImage()

### 전역 변수부
window, canvas, paper = None, None, None
inImage, outImage, circleImage = [], [], []
inH, inW, outH, outW = [0]*4
fullname = ""

### 메인 코드부
window = Tk() # 벽
window.geometry("500x500")
window.resizable(width=False, height=False)
window.title("영상처리 (RC 1)")

# 메뉴 만들기
mainMenu = Menu(window) # 메뉴의 틀
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu,  tearoff=0)  # 상위 메뉴 (파일)
mainMenu.add_cascade(label='파일', menu=fileMenu)
fileMenu.add_command(label='열기', command=openImage)
fileMenu.add_command(label='저장', command=saveImage)
fileMenu.add_separator()
fileMenu.add_command(label='종료', command=window.quit())

pixelMenu = Menu(mainMenu,  tearoff=0)  # 상위 메뉴 (화소점 처리)
bwMenu = Menu(pixelMenu,  tearoff=0)  # 하위 메뉴 (흑백 처리)
paraMenu = Menu(pixelMenu,  tearoff=0)  # 하위 메뉴 (파라볼라 처리)
calMenu = Menu(pixelMenu,  tearoff=0)  # 하위 메뉴 (논리 연산자 처리)
mainMenu.add_cascade(label='화소점 처리', menu=pixelMenu)
pixelMenu.add_command(label='동일 이미지', command=equalImage)
pixelMenu.add_command(label='밝게/어둡게', command=addImage)
pixelMenu.add_command(label='반전', command=reverseImage)
pixelMenu.add_cascade(label='흑백', menu=bwMenu)
bwMenu.add_command(label='흑백 (127 기준)', command=bwImage)
bwMenu.add_command(label='흑백 (평균값)', command=bwAvgImage)
bwMenu.add_command(label='흑백 (중앙값)', command=bwMedImage)
pixelMenu.add_cascade(label='감마', command=gammaImage)
pixelMenu.add_cascade(label='파라볼라', menu=paraMenu)
paraMenu.add_cascade(label='CAP형', command=paraCapImage)
paraMenu.add_cascade(label='CUP형', command=paraCupImage)
pixelMenu.add_cascade(label='논리 연산자', menu=calMenu)
calMenu.add_cascade(label='AND', command=andImage)
calMenu.add_cascade(label='OR', command=orImage)
calMenu.add_cascade(label='XOR', command=xorImage)

geomatricMenu = Menu(mainMenu,  tearoff=0)  # 상위 메뉴 (기하학 처리)
zoomOutMenu = Menu(geomatricMenu,  tearoff=0)  # 하위 메뉴 (줌아웃 처리)
zoomInMenu = Menu(geomatricMenu,  tearoff=0)  # 하위 메뉴 (줌인 처리)
rotateMenu = Menu(geomatricMenu,  tearoff=0)  # 하위 메뉴 (회전 처리)
mirrorMenu = Menu(geomatricMenu,  tearoff=0)  # 하위 메뉴 (미러링 처리)
mainMenu.add_cascade(label='기하학 처리', menu=geomatricMenu)
geomatricMenu.add_cascade(label='줌아웃', menu=zoomOutMenu)
zoomOutMenu.add_command(label='줌아웃', command=zoomOutImage)
zoomOutMenu.add_command(label='줌아웃 (중앙값)', command=zoomOutAvgImage)
zoomOutMenu.add_command(label='줌아웃 (평균값)', command=zoomOutMedImage)
geomatricMenu.add_cascade(label='줌인', menu=zoomInMenu)
zoomInMenu.add_command(label='줌인 (포워딩)', command=zoomInImage)
zoomInMenu.add_command(label='줌인 (백워딩)', command=zoomIn2Image)
zoomInMenu.add_command(label='줌인 (양선형)', command=zoomInYSImage)
geomatricMenu.add_cascade(label='회전', menu=rotateMenu)
rotateMenu.add_command(label='회전 (포워딩)', command=rotateImage)
rotateMenu.add_command(label='회전 (중앙, 백워딩)', command=rotate2Image)
rotateMenu.add_command(label='회전 (중앙, 양선형, 줌인)', command=rotate3Image)
geomatricMenu.add_cascade(label='이동', command=moveImage)
geomatricMenu.add_cascade(label='미러링', menu=mirrorMenu)
mirrorMenu.add_command(label='상하 미러링', command=mirrorUDImage)
mirrorMenu.add_command(label='좌우 미러링', command=mirrorLRImage)

histogramMenu = Menu(mainMenu,  tearoff=0)  # 상위 메뉴 (히스토그램 처리)
mainMenu.add_cascade(label='히스토그램 처리', menu=histogramMenu)
histogramMenu.add_cascade(label='히스토그램 스트레칭', command=histoStretchImage)
histogramMenu.add_cascade(label='엔드인 탐색', command=endInImage)
histogramMenu.add_cascade(label='평활화', command=histoEqualImage)

areaMenu = Menu(mainMenu,  tearoff=0)  # 상위 메뉴 (화소 영역 처리)
pfSharpMenu = Menu(areaMenu,  tearoff=0)  # 하위 메뉴 (주파 필터 처리)
mainMenu.add_cascade(label='화소 영역 처리', menu=areaMenu)
areaMenu.add_cascade(label='엠보싱', command=embossImage)
areaMenu.add_cascade(label='블러링', command=blurImage)
areaMenu.add_cascade(label='샤프닝', command=SharpImage)
areaMenu.add_cascade(label='가우시안', command=gausImage)
areaMenu.add_cascade(label='주파 필터 샤프닝', menu=pfSharpMenu)
pfSharpMenu.add_command(label='고주파', command=hpfSharpImage)
pfSharpMenu.add_command(label='저주파', command=lpfSharpImage)

edgeMenu = Menu(mainMenu,  tearoff=0)  # 상위 메뉴 (경계선 검출)
edgeLocationMenu = Menu(edgeMenu,  tearoff=0)  # 하위 메뉴 (엣지 처리)
mainMenu.add_cascade(label='경계선 검출', menu=edgeMenu)
edgeMenu.add_cascade(label='엣지', menu=edgeLocationMenu)
edgeLocationMenu.add_command(label='수평', command=edgeHorImage)
edgeLocationMenu.add_command(label='수직', command=edgeVerImage)
edgeMenu.add_cascade(label='유사 연산자', command=edgeHomogenImage)
edgeMenu.add_cascade(label='라플라시안', command=laplacianImage)

window.mainloop()
