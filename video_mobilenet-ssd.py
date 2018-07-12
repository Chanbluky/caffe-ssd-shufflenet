
#coding=utf-8

import numpy as np
import sys,os
import cv2
caffe_root = '/home/gjw/caffe-ssd/'
sys.path.insert(0, caffe_root + 'python')  
import caffe  
import time

caffe.set_mode_gpu()   ### 设置GPU模式


net_file= 'shuffleNet/ShuffleNetSSD_deploy.prototxt'  
caffe_model='shuffleNet/model/shufflenet.caffemodel'  


if not os.path.exists(caffe_model):
    print("MobileNetSSD_deploy.caffemodel does not exist,")
    print("use merge_bn.py to generate it.")
    exit()
net = caffe.Net(net_file,caffe_model,caffe.TEST)  

CLASSES = ('background',
           'face')


def preprocess(src):
    img = cv2.resize(src, (300,300))
    img = img - 127.5
    img = img * 0.007843
    return img

def postprocess(img, out):   
    h = img.shape[0]
    w = img.shape[1]
    box = out['detection_out'][0,0,:,3:7] * np.array([w, h, w, h])

    cls = out['detection_out'][0,0,:,1]
    conf = out['detection_out'][0,0,:,2]
    return (box.astype(np.int32), conf, cls)


colours = np.random.rand(32,3)*255

def detect():
    cap = cv2.VideoCapture(0)  # 读取视频

    while (1) :
        ret, origimg = cap.read()
        if ret is False:
            print("Load video error")
            break

        start = time.time()  # fps开始时间

        img = preprocess(origimg)

        img = img.astype(np.float32)
        img = img.transpose((2, 0, 1))

        net.blobs['data'].data[...] = img

        out = net.forward()  #前向传播

        end = time.time()  # fps结束时间
        fps = 1 / (end - start);
        print('FPS = %.2f' % (fps))

        box, conf, cls = postprocess(origimg, out)

        for i in range(len(box)):
           p1 = (box[i][0], box[i][1])
           p2 = (box[i][2], box[i][3])

           cv2.rectangle(origimg, p1, p2, (
                    int(colours[int(cls[i]) % 20, 0]), int(colours[int(cls[i]) % 20, 1]), int(colours[int(cls[i]) % 20, 2])), 2)

        cv2.imshow("SSD", origimg)

        if(cv2.waitKey(1) & 0xff == 27):
                break

if __name__ == '__main__':
    detect()




