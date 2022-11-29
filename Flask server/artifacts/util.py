import base64
import joblib
import numpy as np
import json
import cv2
import pywt

__class_name_to_num = None
__class_num_to_name = None
__mlp_model = None

def classify_img(base64_str):
    # load_artifacts()
    img = base64_string_to_cv2image(base64_str)  # convert to cv2 image from base64 string
    faces = crop_img(img)  # crop the faces from the image
    predictions  = []
    for face_img in faces:  # for each face in the image run make a prediction
        resize_img = cv2.resize(face_img, (128,128))
        face_wav = w2d(face_img, 'db1', 5)
        face_wav = cv2.resize(face_wav, (128,128))
        resize_img = resize_img.reshape(128*128*3, 1)
        face_wav = face_wav.reshape((128*128, 1))
        final_img = np.vstack((resize_img, face_wav))
        final_img = final_img.reshape(1, 128*128*3 + 128*128)
        predictions += [{'class':__class_num_to_name[__mlp_model.predict(final_img)[0]],
                        'prob':np.round(__mlp_model.predict_proba(final_img)*100, 2).tolist()[0],
                        'class_labels': __class_name_to_num}]
    return predictions

def w2d(img, mode='haar', level=1):
    '''
    credit: https://stackoverflow.com/questions/24536552/how-to-combine-pywavelet-and-opencv-for-image-processing
    '''
    imArray = img
    imArray = cv2.cvtColor( imArray,cv2.COLOR_RGB2GRAY )
    imArray =  np.float32(imArray)
    imArray /= 255;
    coeffs=pywt.wavedec2(imArray, mode, level=level)
    coeffs_H=list(coeffs)
    coeffs_H[0] *= 0;
    imArray_H=pywt.waverec2(coeffs_H, mode);
    imArray_H *= 255;
    imArray_H =  np.uint8(imArray_H)
    return imArray_H

def crop_img(img):
    cropped_faces = []
    face_cascade = cv2.CascadeClassifier('../opencv_haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('../opencv_haarcascades/haarcascade_eye.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        crop_img = img[y:y+h, x:x+w]
        crop_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(crop_gray)
        if len(eyes) >= 2:
            cropped_faces += [crop_img]
    return cropped_faces

def base64_string_to_cv2image(base64_str):
    '''
    credit: https://stackoverflow.com/questions/33754935/read-a-base-64-encoded-image-from-memory-using-opencv-python-library
    '''
    encoded_data = base64_str.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def load_artifacts():
    global __class_num_to_name
    global __class_name_to_num
    print("Loading class labels...")
    with open('./artifacts/class_dict.json', 'r') as f:
        __class_name_to_num = json.load(f)
    __class_num_to_name = {val:key for key,val in __class_name_to_num.items()}

    global __mlp_model
    print("Loading saved model...")
    with open('./artifacts/saved_model.pkl', 'rb') as f:
        __mlp_model = joblib.load(f)

# if __name__ == '__main__':
    # load_artifacts()
    # with open("./blackwidow_base64_string.txt", 'r') as f:
    #     base64_str = f.read()
    # pred = classify_img(base64_str)
    # print(pred)