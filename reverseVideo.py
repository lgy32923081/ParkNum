import cv2


def reversePlay(capture, number):

    w = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # fourcc = cv2.VideoWriter_fourcc(*'DIVX') #avi
    fourcc = cv2.VideoWriter_fourcc(*'XVID') #mp4
    # out = cv2.VideoWriter('C:\\HC\\onlyCaptureList\\output5.avi',fourcc,30.0,(int(w),int(h)))
    out = cv2.VideoWriter('C:\\HC\\onlyCaptureList\\reverse' + str(number) + '.mp4', fourcc, 30.0, (int(w), int(h)))

    # check for camera openning
    if capture.isOpened() is False:
        print("Error opening video")

    # Get the total number of frames
    frame_idx = capture.get(cv2.CAP_PROP_FRAME_COUNT) - 1
    print("Starting Frame: '{}'".format(frame_idx))

    # Read until video is finished:
    while capture.isOpened() and frame_idx >= 0:

        # Set the current frame position to start:
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

        # 비디오로부터 프레임을 읽음
        ret, frame = capture.read()

        if ret is True:
            # 동영상 시작될때 이름?
            cv2.imshow('Frame in Reverse', frame)

            out.write(frame)
            # 프레임을 뒤로 감소시키며 거꾸로 재생
            # print("Next index: '{}'".format(frame_idx))
            frame_idx = frame_idx - 1


            # Q를 누르면 꺼짐
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        # Break the while loop
        else:
            out.release()
            break


cap = cv2.VideoCapture("C:\\HC\\folder\\finish_blue.mp4")
reversePlay(cap,0)
cap.release()

cap1 = cv2.VideoCapture("C:\\HC\\folder\\parking1.mp4")
reversePlay(cap1,1)
cap1.release()

cap2 = cv2.VideoCapture("C:\\HC\\folder\\parking2.mp4")
reversePlay(cap2,2)
cap2.release()

cap3 = cv2.VideoCapture("C:\\HC\\folder\\parking3.mp4")
reversePlay(cap3,3)
cap3.release()

cap4 = cv2.VideoCapture("C:\\HC\\folder\\parking4.mp4")
reversePlay(cap4,4)
cap4.release()

cap5 = cv2.VideoCapture("C:\\HC\\folder\\parking5.mp4")
reversePlay(cap5,5)
cap5.release()

cap6 = cv2.VideoCapture("C:\\HC\\folder\\parking6.mp4")
reversePlay(cap6,6)
cap6.release()

cv2.destroyAllWindows()