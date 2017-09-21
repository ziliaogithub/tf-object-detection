from models import object_detection
from config import config
import cv2
import datetime

model_name = config.models["1"]
net = object_detection.Net(graph_fp='%s/frozen_inference_graph.pb' % model_name,
                           labels_fp='data/label.pbtxt',
                           num_classes=90,
                           threshold=0.6)
CAMERA_MODE = 'camera'
STATIC_MODE = 'static'
IMAGE_SIZE = 320


def demo(mode=CAMERA_MODE):
    if mode == STATIC_MODE:
        img_fp = 'test_images/1.jpg'
        img = cv2.imread(img_fp)
        net.predict(img=img, display_img=img)
        cv2.waitKey()
        cv2.destroyAllWindows()
    elif mode == CAMERA_MODE:
        cap = cv2.VideoCapture(0)

        while True:
            start = datetime.datetime.now().microsecond*0.001
            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (IMAGE_SIZE, IMAGE_SIZE))
            net.predict(img=resized_frame, display_img=frame)
            end = datetime.datetime.now().microsecond*0.001
            elapse = end - start
            print 'Elapse: ', elapse, ' ms'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    demo(mode=CAMERA_MODE)
