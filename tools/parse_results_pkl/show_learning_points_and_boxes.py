# -*- coding: utf-8 -*-
import pickle
import cv2
import json
import os 
import shutil
import numpy as np 

detection_pkl_path = 'work_dirs/r50_dotav1/results.pkl'
val_json = 'data/dataset_demo_split/test_datasetdemo.json'

outpath = 'work_dirs/r50_dotav1/vis_result/'
inputpath = 'data/dataset_demo_split/images/'

if os.path.exists(outpath):
    shutil.rmtree(outpath)  # delete output folderX
    
os.makedirs(outpath)

conf_thresh = 0.2
def transfer_to_order_point(corner_points):
    a_x = corner_points[0][0]
    a_y = corner_points[0][1]

    b_x = corner_points[1][0]
    b_y = corner_points[1][1]

    c_x = corner_points[2][0]
    c_y = corner_points[2][1]

    d_x = corner_points[3][0]
    d_y = corner_points[3][1]

    # top x0 y0
    if  a_y == min(a_y, b_y, c_y, d_y) :
        x0 = a_x
        y0 = a_y
    if  b_y == min(a_y, b_y, c_y, d_y) :
        x0 = b_x
        y0 = b_y
    if  c_y == min(a_y, b_y, c_y, d_y) :
        x0 = c_x
        y0 = c_y
    if  d_y == min(a_y, b_y, c_y, d_y) :
        x0 = d_x
        y0 = d_y

    # right x1 y1
    if  a_x == max(a_x, b_x, c_x, d_x) :
        x1 = a_x
        y1 = a_y
    if  b_x == max(a_x, b_x, c_x, d_x) :
        x1 = b_x
        y1 = b_y
    if  c_x == max(a_x, b_x, c_x, d_x) :
        x1 = c_x
        y1 = c_y
    if  d_x == max(a_x, b_x, c_x, d_x) :
        x1 = d_x
        y1 = d_y

    # bottom x2 y2
    if  a_y == max(a_y, b_y, c_y, d_y) :
        x2 = a_x
        y2 = a_y
    if  b_y == max(a_y, b_y, c_y, d_y) :
        x2 = b_x
        y2 = b_y
    if  c_y == max(a_y, b_y, c_y, d_y) :
        x2 = c_x
        y2 = c_y
    if  d_y == max(a_y, b_y, c_y, d_y) :
        x2 = d_x
        y2 = d_y

    # left x3 y3
    if  a_x == min(a_x, b_x, c_x, d_x) :
        x3 = a_x
        y3 = a_y
    if  b_x == min(a_x, b_x, c_x, d_x) :
        x3 = b_x
        y3 = b_y
    if  c_x == min(a_x, b_x, c_x, d_x) :
        x3 = c_x
        y3 = c_y
    if  d_x == min(a_x, b_x, c_x, d_x) :
        x3 = d_x
        y3 = d_y

    order_points = np.array([(x0,y0),(x1,y1),(x2,y2),(x3,y3)], np.int32)
    return order_points


#open result pkl
with open(detection_pkl_path, 'rb') as file:
    while True:
        try:
            data = pickle.load(file)  # list[num_epoch/batch_size * list[batch_size * list[num_classes * array(n, [18, 8, score])]][0] ]
        except EOFError:
            break

num_img = len(data)

#open json 
with open(val_json) as f:
    ann=json.load(f)

    for img_item in ann['images']:  # 遍历每张图
        #print('img id:', img_item['id'])
        index_img = img_item['id'] - 1
        img_results = data[index_img]

        img_name = img_item['file_name']
        img_base_name = img_name.split('.png')[0]   # 'P0003__1.0__0___0'
        bboxes = img_results  # bboxes： list[num_classes * array(n, [18, 8, score])]
        num_bboxes = len(bboxes)

        for iter_box in range(num_bboxes): # 遍历每个类的检测结果

            if len(bboxes[iter_box])>0:
                #print(bboxes[iter_box])
                if iter_box == 0:
                    class_name = 'plane'
                    r_color = (0, 0, 255) #纯红
                elif iter_box == 1:
                    class_name = 'baseball-diamond'
                    r_color = (0, 255, 0) #纯绿
                elif iter_box == 2:
                    class_name = 'bridge'
                    r_color = (255, 0, 0) # 纯蓝
                elif iter_box == 3:
                    class_name = 'ground-track-field' 
                    r_color = (169, 169, 169) # 深灰色
                elif iter_box == 4:
                    class_name = 'small-vehicle'
                    r_color = (0, 0, 139) #深红色
                elif iter_box == 5:
                    class_name = 'large-vehicle'
                    r_color = (0, 69, 255) #橙红色
                elif iter_box == 6:
                    class_name = 'ship'
                    r_color = (30, 105, 210)# 巧克力色
                elif iter_box == 7:
                    class_name = 'tennis-court'
                    r_color = (10,215,255) #金色
                elif iter_box == 8:
                    class_name = 'basketball-court'
                    r_color = (0,128,128) #橄榄色
                elif iter_box == 9:
                    class_name = 'storage-tank'
                    r_color = (203,192,255) #粉色
                elif iter_box == 10:
                    class_name = 'soccer-ball-field'
                    r_color = (230,216,173) #天蓝色
                elif iter_box == 11:
                    class_name = 'roundabout' 
                    r_color = (238,130,238) #紫罗兰
                elif iter_box == 12:
                    class_name = 'harbor'
                    r_color = (144,238,144) #浅绿
                elif iter_box == 13:
                    class_name = 'swimming-pool'
                    r_color = (130,0,75) #藏青色
                elif iter_box == 14:
                    class_name = 'helicopter'  
                    r_color = (147,20,255) #深粉色
                elif iter_box == 15:
                    class_name = 'container-crane'  
                    r_color = (255,0,255) #????
                elif iter_box == 16:
                    class_name = 'airport'  
                    r_color = (255,255,0) #
                elif iter_box == 17:
                    class_name = 'helipad'  
                    r_color = (0,255,255) #
                else:
                    class_name = None
                    print('Unknown class_name!!!!!!!!!!!!!!!!!!!!!!! ')
                    
                    
                for bbox in bboxes[iter_box]:  # bboxes[iter_box]：  array(n, [18, 8, score]) x_first # 遍历每个bbox
                
                    pt_x = bbox[0:-9:2]  # (start_index:end_index:step) 取points 的x坐标
                    pt_y = bbox[1:-9:2]  # (start_index:end_index:step) 取points 的y坐标
                
                    confidence = float(bbox[-1])

                    #confidence threshold
                    if confidence > conf_thresh:
                        if os.path.exists(outpath+img_name):
                            #print(img_name)
                            image = cv2.imread(outpath+img_name)
                        
                        else:
                            image = cv2.imread(inputpath+img_name)
                        
                        # visulize the oriented boxes     
                        box_list = []
                        box_list.append((float(bbox[-9]), float(bbox[-8])))
                        box_list.append((float(bbox[-7]), float(bbox[-6])))
                        box_list.append((float(bbox[-5]), float(bbox[-4])))
                        box_list.append((float(bbox[-3]), float(bbox[-2])))  # box_list.size(4, 2)
                        box_order = transfer_to_order_point(box_list)  # 给四个点排序
                        cv2.polylines(image, [box_order], True, r_color, thickness=1)  # 四个点连线

                        for i in range(len(pt_x)):
                            # learning points 
                            cv2.circle(img=image, center=(int(pt_x[i]), int(pt_y[i])), radius=1, color=r_color, thickness=2)  # 画点

                        text_label = '%s %.2f' % (class_name, confidence)
                        cv2.putText(image, text_label,  
                                    (int((box_order[1][0] + box_order[3][0])/2), int((box_order[0][1] + box_order[2][1])/2) - 0),
                                    0, 0.25, r_color, thickness=1, lineType=cv2.LINE_AA)
                        cv2.imwrite(outpath+img_name, image)