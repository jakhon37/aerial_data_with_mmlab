
import json
import os 
import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = '/Users/jakhon37/pyProjects/data_test/aerial_data/image/TS_FGT_512/LC_JJ_SN_33606_001_20190503_FGT.tif'

if os.path.isfile(image_path):  # 이미지 파일이 존재하는지 확인
    image_array = cv2.imread(image_path)
    zero_mask = np.zeros(image_array.shape[0:3])
    masked_image = zero_mask
    
    
json_path = 'aerial_data/label/TL_FGT_512/FGT_512_Json/LC_JJ_SN_33606_001_20190503_FGT.json'
with open(json_path) as file:
    json_read = json.load(file)

print('number of dicts in json file is: ' , len(json_read))
print('test ', len(json_read['features']))
for feature in json_read['features']:
    building_imcoords = feature['geometry']['coordinates'][0]
    
    polygon = np.array(building_imcoords)
    polygon = np.array(polygon, np.float32)
    polygon = np.array(polygon, np.int32)
    cv2.fillPoly(masked_image, np.int32([polygon]), [128, 64, 128])

# print('current file: {}'.format(building_label))
plt.imshow(masked_image)
plt.show()
        
        
print(f'printing coord for test: {building_imcoords}')






print('len of masked image array: ', len(masked_image))

# cv2.imshow('image', image_array)

# cv2.waitKey(0)
# cv2.destroyAllWindows()





