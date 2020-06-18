from time import sleep

import cv2
from darkflow.net.build import TFNet

import threading
import os, io

import parkNumPackage.firebase
from ParkNum.parkNumPackage import firebase

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/VisionAPI/sehoon.json"

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

options = {
    'model': 'C:\\HC\\darkflow\\cfg\\parking-yolo-obj.cfg',
    'load': 'C:\\HC\\darkflow\\bin\\parking20_06_12_2000jpg.weights',
    'threshold': 0.6
}  # weights파일, cfg파일 설정


# -----------환경설정부분----------


# ------------변수선언부분-----------
# height, width, number of channels in image
# height = img.shape[0]
# # width = img.shape[1]
# # channels = img.shape[2]
# -----------참고부분 -----

# OCR돌리는 함수
def detect_text(num):
    fw = open('C:\\HC\\afterCrop\\ocr' + str(num) + '.text', 'w', -1, "utf-8")
    vstr = ""

    path = os.path.join(
        os.path.dirname(__file__),
        'C:\\HC\\afterCrop\\cropYolo' + str(num) + '.jpg')

    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\nCropImg로 부터 "{}" 텍스트를 추출 하였습니다.'.format(text.description))
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                     for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))
        vstr = vstr + str(text.description) + "\n"
    try:
        fw.writelines(vstr.split("\n")[0] + "\t" + vstr.split("\n")[1])
        fw.close()
    except IndexError:
        fw.write("parknum is not found")
        fw.close()


# 최신 동영상 파일 찾는 함수
def find_recent_video():
    files_path = "C:\\HC\\videoList\\"
    file_list = []
    for f_name in os.listdir(f"{files_path}"):
        written_time = os.path.getctime(f"{files_path}{f_name}")
        file_list.append((f_name, written_time))
    # 생성시간 역순으로 정렬
    sorted_file_list = sorted(file_list, key=lambda x: x[1], reverse=True)
    # 가장 앞에있는 파일을 넣어줌
    recent_file = sorted_file_list[0]  # 첫번째꺼.
    recent_file_name = recent_file[0]
    check_video_path = files_path + str(recent_file_name)

    return check_video_path


def cropTextImg(index):
    # read 는 cv2함수 open pil함수
    img = cv2.imread("C:\\HC\\imgList\\" + "CarLocationImg_" + str(index) + ".jpg", cv2.IMREAD_UNCHANGED)
    # img = cv2.imread("C:\\HC\\imgList\\" + "test_" + str(index) + ".jpg", cv2.IMREAD_GRAYSCALE)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = tfnet.return_predict(img)
    if result == list():
        print("텍스트를 찾지 못햇습니다.")
        return 0
    else:
        cropImg = img.copy()

        imgHeight = img.shape[0]
        imgWidth = img.shape[1]
        flag = True

        topleftX = result[0]['topleft']['x']
        topleftY = result[0]['topleft']['y']
        bottomRightX = result[0]['bottomright']['x']
        bottomRightY = result[0]['bottomright']['y']

        if (topleftX - 40) > 0:
            topleftX = topleftX - 40

        if (bottomRightX + 40) < imgWidth:
            bottomRightX = bottomRightX + 40

        if (topleftY - 40) > 0:
            topleftY = topleftY - 40

        if (bottomRightY + 40) < imgHeight:
            bottomRightY = bottomRightY + 40

        cropImg = img[int(topleftY):int(bottomRightY), int(topleftX):int(bottomRightX)]
        # cropImg = img[0:100, 300:400]

        # print("위 topleftX 값 : " + str(topleftX) + "\n")
        # print("위 topleftY 값 : " + str(topleftY) + "\n")
        # print("아래 bottomRightX 값 : " + str(bottomRightX) + "\n")
        # print("아래 bottomRightY 값 : " + str(bottomRightY) + "\n")
        print("C:\\HC\\afterCrop\\cropYolo" + str(index) + ".jpg를 성공적으로 저장 했습니다.")
        cv2.imwrite("C:\\HC\\afterCrop\\cropYolo" + str(index) + ".jpg", cropImg)

    cv2.destroyAllWindows()


def reversePlay(capture):
    global timer_end_flag
    global find_parknum_flag
    listNumber = 1
    captureCount = 1
    frameController = 0
    frameDelay = 0

    # check for camera openning
    if capture.isOpened() is False:
        print("Error opening video")

    # Get the total number of frames
    frame_idx = capture.get(cv2.CAP_PROP_FRAME_COUNT) - 1
    before_frame_idx = frame_idx
    Out_In_decision()
    # 시작 프레임을 출력하는 메소드
    # print("Starting Frame: '{}'".format(frame_idx))
    if frame_idx > 5000:
        frameController = 30
        frameDelay = frameController * 10
    elif frame_idx > 1500:
        frameController = 30
        frameDelay = frameController * 8
    else :
        frameController = 30
        frameDelay = frameController * 4


    # Read until video is finished:
    while capture.isOpened() and frame_idx >= 0:

        # Set the current frame position to start:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

        # 비디오로부터 프레임을 읽음
        ret, frame = capture.read()

        if ret is True:
            # 동영상 시작될때 이름?
            cv2.imshow('Frame in Reverse', frame)

            results = tfnet.return_predict(frame)

            if before_frame_idx > frame_idx:
                if len(results) > 0:
                    if results[0]['label'] == 'parknum':
                        cv2.imwrite("C:\\HC\\imgList\\" + "CarLocationImg_" + str(listNumber) + ".jpg", frame)
                        captureCount += 1
                        listNumber += 1
                        # 420프레임동안은 같은 사진을 찍지 않겠다.
                        before_frame_idx -= frameDelay
                        print("주차 위치로 부터 기둥 사진을 저장 했습니다.")
                        if not find_parknum_flag:
                            find_parknum_flag = True

                    # 사진을 3개저장하면종료.
                    if captureCount > 3:
                        timer_end_flag = True
                        return captureCount
                        break
                # for result in results:
                #     if result['label'] == 'parknum':
                #         cv2.imwrite("C:\\HC\\imgList\\" + "cropImg_" + str(listNumber) + ".jpg", frame)
                #         captureCount += 1
                #         listNumber += 1
                #         # 100프레임동안은 같은 사진을 찍지 않겠다.
                #         before_frame_idx -= 100
                #         print("주차 위치로 부터 기둥 사진을 저장 했습니다.")
                #         find_parknum_flag = True
                #
                #     # 사진을 3개저장하면종료.
                #     if captureCount > 3:
                #         return captureCount
                #         break

            # 프레임을 뒤로 감소시키며 거꾸로 재생
            # print("Next index: '{}'".format(frame_idx))
            # print("beform_frame index: '{}'".format(before_frame_idx))
            frame_idx = frame_idx - frameController

            if count > 10 and (find_parknum_flag == False):
                capture.release()
                return 0

            # Q를 누르면 꺼짐
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        # Break the while loop
        else:
            break


def Out_In_decision():
    global count
    global timer_end_flag
    global find_parknum_flag
    timer = threading.Timer(1, Out_In_decision)
    timer.start()

    count += 1
    # print("경과 시간 : " + str(count))
    # if find_parknum_flag == True:
    #     timer.cancel()
    if timer_end_flag:
        timer.cancel()
        timer_end_flag = False

    if count > 10 and (find_parknum_flag == False):
        timer.cancel()
        sleep(1)
        reversePlay_OnlyCapture()
        count = 0


def reversePlay_OnlyCapture():
    listNumber = 1
    captureCount = 1
    capture = cv2.VideoCapture(find_recent_video())

    # check for camera openning
    if capture.isOpened() is False:
        print("Error opening video")

    # Get the total number of frames
    frame_idx = capture.get(cv2.CAP_PROP_FRAME_COUNT) - 1

    if frame_idx > 5000:
        frameController = 30
        frameDelay = frameController * 10
    elif frame_idx > 1500:
        frameController = 30
        frameDelay = frameController * 8
    else :
        frameController = 30
        frameDelay = frameController * 4

    # 시작 프레임을 콘솔창에 찍어주는 메소드
    # print("Starting Frame: '{}'".format(frame_idx))

    # Read until video is finished:
    while capture.isOpened() and frame_idx >= 0:

        # Set the current frame position to start:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

        # 비디오로부터 프레임을 읽음
        ret, frame = capture.read()

        if ret is True:

            # cv2.imshow('Frame in Reverse', frame)

            cv2.imwrite("C:\\HC\\imgList\\" + "parkImg_" + str(listNumber) + ".jpg", frame)
            captureCount += 1
            listNumber += 1

            # 사진을 3개저장하면종료.
            if captureCount > 3:
                break

            # 프레임을 뒤로 감소시키며 거꾸로 재생
            print("Next index: '{}'".format(frame_idx))
            frame_idx = frame_idx - frameController - 30

            # Q를 누르면 꺼짐
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        # Break the while loop
        else:
            break


def remove_Forder():
    afterCrop_folder_path = "C:\\HC\\afterCrop\\"
    imgList_folder_path = "C:\\HC\\imgList\\"

    for f_name in os.listdir(f"{afterCrop_folder_path}"):
        os.remove(afterCrop_folder_path + f_name)

    for f_name in os.listdir(f"{imgList_folder_path}"):
        os.remove(imgList_folder_path + f_name)


# capture = cv2.VideoCapture(find_recent_video())
# capture = cv2.VideoCapture('C:\\HC\\videoList\\road1.mp4')
tfnet = TFNet(options)

timer_end_flag = False
find_parknum_flag = False
saveCount = 0
count = 0


def Main():
    remove_Forder()
    capture = cv2.VideoCapture(find_recent_video())
    saveCount = reversePlay(capture)
    for i in range(1, saveCount):
        try:
            cropTextImg(i)
            detect_text(i)
        except IndexError:
            i += 1

    capture.release()
    cv2.destroyAllWindows()
    firebase.main()


Main()
