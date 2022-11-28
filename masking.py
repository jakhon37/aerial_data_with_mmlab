import os
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import pylab
# %matplotlib inline

 
# building_imgs_path = '/content/drive/MyDrive/LV2_dataset/LV2_validation_set/images'
# building_labels_path = '/content/drive/MyDrive/LV2_dataset/LV2_validation_set/labels/building'

building_imgs_path = '/Users/jakhon37/pyProjects/data_test/aerial_data/image/TS_FGT_512'
building_labels_path = '/Users/jakhon37/pyProjects/data_test/aerial_data/label/TL_FGT_512/FGT_512_Json'

save_dir = '/out_mask'  # 마스킹 이미지를 저장할 위치

building_labels_list = os.listdir(building_labels_path)
print(f'list of building: {len(building_labels_list)}')
def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

for building_label in building_labels_list:
    print(len(building_label))
    # json 파일인지 체크
    if building_label.split('.')[1] != 'json':
        print('empty buildinnng ccooords')
        continue

    building_img = os.path.join(building_imgs_path, building_label.split('.')[0] + '.png')
    print(building_img)
    if os.path.isfile(building_img):  # 이미지 파일이 존재하는지 확인
        image_array = cv2.imread(building_img)
        zero_mask = np.zeros(image_array.shape[0:3])
        masked_image = zero_mask

        cur_build_json = pd.read_json(building_labels_path + "/" + building_label)

        for feature in cur_build_json['features']:
            # building_imcoords = feature['properties']['building_imcoords']
            building_imcoords = feature['geometry']['coordinates'][0]
            if len(building_imcoords) == 0:  # 좌표 정보가 없을 경우 다음 좌표 정보 확인
                continue

            building_imcoords_list = building_imcoords.split(',')
            building_imcoords_list = list_chunk(building_imcoords_list, 2)

            polygon = np.array(building_imcoords_list)
            polygon = np.array(polygon, np.float32)
            polygon = np.array(polygon, np.int32)
            cv2.fillPoly(masked_image, np.int32([polygon]), [0, 128, 128])

        # road_json = os.path.join(road_labels_path, building_label)
        # if os.path.isfile(road_json):  # 도로 json 파일이 존재하는지 확인
        #     cur_road_json = pd.read_json(road_json)

        #     for feature in cur_road_json['features']:
        #         road_imcoords = feature['properties']['road_imcoords']

        #         if len(road_imcoords) == 0:  # 좌표 정보가 없을 경우 다음 좌표 확인
        #             continue
                
        #         road_imcoords_list = road_imcoords.split(',')
        #         road_imcoords_list = list_chunk(road_imcoords_list, 2)

        #         polygon = np.array(road_imcoords_list)
        #         polygon = np.array(polygon, np.float32)
        #         polygon = np.array(polygon, np.int32)
        #         cv2.fillPoly(masked_image, np.int32([polygon]), [128, 64, 128])

        print('current file: {}'.format(building_label))
        plt.imshow(masked_image)
        plt.show()

        save_path = os.path.join(save_dir, building_label.split('.')[0] + '.png')
        result = cv2.imwrite(save_path, masked_image)

        if result == True:
            print('File saved successfully\n')
        else:
            print('{} file: Error in saving file\n'.format(save_path))