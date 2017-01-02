"""Click on pendulum videos to get trajectories frame by frame"""
import cv2


def show_video(filename="data/pendule_simple_10cm_m.avi"):
    # cv2.startWindowThread()
    cap = cv2.VideoCapture(filename)
    while cap.isOpened():
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # cv2.destroyAllWindows()


show_video()
