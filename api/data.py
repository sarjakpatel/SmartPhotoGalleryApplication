#libraries
#to compute encodings
import cv2
import face_recognition
from PIL import Image
from fer import FER
from deepface import DeepFace
import requests
import PIL
#to store encodings
import firebase_admin
from firebase_admin import credentials, firestore
import json
import pyrebase
import replicate
import base64
import os
import io
import tensorflow as tf
import replicate
from transformers import ViltProcessor, ViltForQuestionAnswering
import torch
from torchvision import transforms
import pytesseract
import scipy.ndimage
import matplotlib.pyplot as plt
import openai


pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'


cred_file_path = "fbAdminConfig.json"
cred = credentials.Certificate(cred_file_path)
firebase_admin.initialize_app(cred)


# this connects to our Firestore database
db = firestore.client() 

firebase = pyrebase.initialize_app(json.load(open('fbconfig.json')))
storage = firebase.storage()


#cascade_file_path = "C:/Users/HP/Downloads/data/haarcascades/haarcascade_frontalface_alt2.xml"
cascade_file_path = r"cascades/data/haarcascades/haarcascade_frontalface_alt2.xml"
face_cascade = cv2.CascadeClassifier(cascade_file_path)


app = replicate.Client(api_token="r8_daJhrGf2aItg54dmXvEohNelrWaNeq72OKBrG")

#change this
openai.api_key = ""



def compute_face_encodings(input):

    if isinstance(input, str):

        img = Image.open(requests.get(input, stream=True).raw)

        img = cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    
    else:

        #file_name_string = base64.urlsafe_b64encode(url)
        #pil_image = PIL.Image.open(input)
        img = cv2.cvtColor(numpy.array(input), cv2.COLOR_RGB2BGR)
        #img = cv2.imread(input)
        # img = input
    
    #img = cv2.imread(opencvImage)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=8)
    
    for x, y, w, h in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 0)

    #print(len(faces))
    
    print('Number of faces detected:', len(faces))

    if len(faces)>0:
        
        
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]

        encoding = face_recognition.face_encodings(rgb, boxes)

        print('Computed encodings')
    
        return encoding
    
    else:
        
        return []#returns ndarray




def store_cropped_image(email, image_url, token):

    img_format = Image.open(requests.get(image_url, stream=True).raw)
    
    img = cv2.cvtColor(numpy.array(img_format), cv2.COLOR_RGB2BGR)
    

    #img = cv2.imread(opencvImage)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    faces = face_cascade.detectMultiScale(grey, scaleFactor=1.3, minNeighbors=8)
    #print(faces)

    #print(len(faces))

    if (len(faces) > 0):
        urls = []
        keys = []
        #print(i_val)
        for i in range(len(faces)):
            
            (x, y, w, h) = faces[i]
            

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 0)
        

            #boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]
            boxes = [(y, x + w, y + h, x)]
            face_encoding = face_recognition.face_encodings(rgb, boxes)
            
            face = img[y:y + h, x:x + w]

            url_ref = db.collection("userDetails").document(email).collection("data")
            # Add documents to the subcollection.
            url1_ref = url_ref.document("cropped_face_url")
            prev_stored_urls = url1_ref.get().to_dict()

            url_ref = db.collection("userDetails").document(email).collection("data")
            encodings_ref = url_ref.document("face_encodings")
            prev_stored_encodings = encodings_ref.get().to_dict()

            url_ref = db.collection("userDetails").document(email).collection("data")
            image_urls_ref = url_ref.document("image_urls")
            prev_stored_image_urls = image_urls_ref.get().to_dict()
            

            if prev_stored_urls:
                length = len(prev_stored_urls)

            else:
                length = 0
            
            file_path = email + "_face_" + str(length) + ".jpg"
            ####################
            cv2.imwrite(file_path, face)

            res = storage.child(file_path).put(file_path)

            # Get url of image
            url = storage.child(file_path).get_url(token)
            urls.append(url)

            #store face url to firebase db
            if prev_stored_urls:
                length = len(prev_stored_urls)
                key = str(length)
                url1_ref.update({key : url})
                keys.append(key)
                face_encoding = numpy.array(face_encoding)
                face_encoding = numpy.array2string(face_encoding, separator=',', suppress_small = True)
                encodings_ref.update({key: face_encoding})

                image_urls_ref.update({key: [image_url]})
            
                print('Added face url to the firebase db')
                #return 'done'

        
            #when the first encoding is stored in a user's account
            else:
                
                key = '0'
                url1_ref.set({key : url})
                keys.append(key)
                face_encoding = numpy.array(face_encoding)
                face_encoding = numpy.array2string(face_encoding, separator=',', suppress_small = True)
                encodings_ref.set({key: face_encoding})

                image_urls_ref.set({key: [image_url]})
                print('Added first face url to the firebase db')
                #return 'done'
                        
        return urls, keys
        
    else:
        
        #no faces encoded
        return [], []




def search_similar_image(email, image_url):

    faces = compute_face_encodings(image_url)
    flag = 0
    if len(faces)>0:
        
        flag = 1
        print('Computed face encodings for a given image url')
        faces1 = len(faces)

        doc_ref = db.collection("userDetails").document(email).collection("data")
        print('Database connected')
        encoding_ref = doc_ref.document("face_encodings")
        stored_encodings = encoding_ref.get().to_dict()

        doc_ref = db.collection("userDetails").document(email).collection("data")
        url_ref = doc_ref.document("image_urls")
        stored_urls = url_ref.get().to_dict()

        dict_of_encodings = {}
        
    
        output_urls = []

        if stored_encodings:
            match1 = []

            for key in stored_encodings.keys():
                encoding = stored_encodings[key]
                #stored encoding type coversion
                encoding = encoding.replace('[', '').replace(']', '').replace('\n', '')
                new_encoding = list(encoding.split(","))
                new_encoding1 = [eval(i) for i in new_encoding]
                dict_of_encodings.update({key : new_encoding1})
            print('Collected all encodings from the firebase')
            #print(dict_of_encodings)
            
            keys = []
        
            for face_encoding1 in faces:
                i = 0
                for key in dict_of_encodings.keys():
                    
                    face_encoding2 = dict_of_encodings[key]


                    face_encoding1 = numpy.array(face_encoding1)
                    face_encoding2 = numpy.array(face_encoding2)

                    matches = face_recognition.compare_faces([face_encoding1], face_encoding2, tolerance = 0.5)
                    is_match = any(matches)
                    
                    print('Are faces matching:', is_match)

                    if is_match:
                        current_url = stored_urls[key]
                        output_urls.append(current_url)
                        keys.append(key)
                        match1 = True
                    
            return output_urls, keys, match1, flag
        
        else:
            return output_urls, None, False, flag
    else:
        #no encodings found
        return [], [], False, flag




def check_encodings(email, image_url, token):

    urls, keys, is_match, flag = search_similar_image(email, image_url)
    if flag == 0:
        return False
    
    else:

        print('Face matched?', is_match)
        
        doc_ref = db.collection("userDetails").document(email).collection("data")
        print('Database connected')

        url_ref = doc_ref.document("image_urls")
        stored_urls = url_ref.get().to_dict()
        
        
        if is_match:
                
            for key in keys:
        
                url_ref.update({key: firestore.ArrayUnion([image_url])})
            print("Given image encodings matched with the stored encodings so updated image_urls hashmap")
            
            return True

        else:

            store_cropped_image(email, image_url, token)

            return True




def deblur_image1(input_image):

    image = cv2.cvtColor(numpy.array(input_image), cv2.COLOR_BGR2RGB)
 

    kernel = numpy.array([[0,-1,0], [-1,5,-1], [0,-1,0]])

    sharpened = cv2.filter2D(image, -1, kernel)

    img = cv2.cvtColor(sharpened, cv2.COLOR_BGR2RGB)
    img = PIL.Image.fromarray(img)

    return img




def ocr_core(filename):  
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text




def compute_emotion(input):
    detector = FER(mtcnn=True)
    img = cv2.cvtColor(numpy.array(input), cv2.COLOR_RGB2BGR)
    emotion = detector.detect_emotions(img)
    print(emotion)
    dominant_emotion = detector.top_emotion(img)
    return dominant_emotion



def analyze_face(input):
    img = cv2.cvtColor(numpy.array(input), cv2.COLOR_RGB2BGR)
    face_analysis = DeepFace.analyze(img_path = img, enforce_detection=False)
    return [
        "Age : " + str(face_analysis[0]['age']),
        "Race : " + str.capitalize(face_analysis[0]['dominant_race']),
        "Emotion : " + str.capitalize(face_analysis[0]['dominant_emotion']),
        "Gender : " + face_analysis[0]['dominant_gender']
    ]






#https://replicate.com/sanzgiri/cartoonify
def image_cartoonify1(image, reuse = True):

    image.save(r'output/cartoonify.jpg')
    input_img = r'output/cartoonify.jpg'
    path = open(input_img, "rb")
    
    output = app.run("sanzgiri/cartoonify:a6f24cf966b84dc3959b9c84f6f5739287b243bc85d5d2f5fb0a9ca9eb6a0f0a",
    input= {"infile": path})
    #os.remove('img.jpg')

    img = Image.open(requests.get(output, stream=True).raw)
    #print(output)
    return img




#https://huggingface.co/dandelin/vilt-b32-finetuned-vqa
def image_question1(image, question):

    # prepare image + question
    url = "http://images.cocodataset.org/val2017/000000039769.jpg"
    #image = Image.open(requests.get(url, stream=True).raw)
    #text = "How many cats are there?"
    #print(type(image))

    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    # prepare inputs
    encoding = processor(image, question, return_tensors="pt")

    # forward pass
    outputs = model(**encoding)
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    print("Predicted answer:", model.config.id2label[idx])
    result = model.config.id2label[idx]

    print(result)

    return result




#image = r"C:\Users\HP\OneDrive\Documents\Snapchat-644617226.jpg"
#photo_to_sketch(image)




#https://huggingface.co/spaces/eugenesiow/remove-bg/blob/main/app.py
def remove_img_bg(image):

    def make_transparent_foreground(pic, mask):
        # split the image into channels
        b, g, r = cv2.split(numpy.array(pic).astype('uint8'))
        # add an alpha channel with and fill all with transparent pixels (max 255)
        a = numpy.ones(mask.shape, dtype='uint8') * 255
        # merge the alpha channel back
        alpha_im = cv2.merge([b, g, r, a], 4)
        # create a transparent background
        bg = numpy.zeros(alpha_im.shape)
        # setup the new mask
        new_mask = numpy.stack([mask, mask, mask, mask], axis=2)
        # copy only the foreground color pixels from the original image where mask is set
        foreground = numpy.where(new_mask, alpha_im, bg).astype(numpy.uint8)

        return foreground


    def remove_background(input_image):
        preprocess = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        input_tensor = preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0)  # create a mini-batch as expected by the model

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            model.to('cuda')

        with torch.no_grad():
            output = model(input_batch)['out'][0]
        output_predictions = output.argmax(0)

        # create a binary (black and white) mask of the profile foreground
        mask = output_predictions.byte().cpu().numpy()
        background = numpy.zeros(mask.shape)
        bin_mask = numpy.where(mask, 255, background).astype(numpy.uint8)

        foreground = make_transparent_foreground(input_image, bin_mask)

        return foreground, bin_mask


    def inference(img):
        print(type(img))
        #image = Image.open(img)
        foreground, _ = remove_background(img)

        PIL_image = Image.fromarray(numpy.uint8(foreground)).convert('RGB')
        PIL_image.save(r'output/remove_bg_image.jpg')
        return PIL_image

    model = torch.hub.load('pytorch/vision:v0.6.0', 'deeplabv3_resnet101', pretrained=True)
    model.eval()
    result_img = inference(image)



    return result_img


#image = "cartoonify.jpg"
#image = Image.open(image)
#print(inference(image))



#https://github.com/rra94/sketchify/blob/master/sketchify.ipynb
def img_sketch(image):

    def dodge(front,back):

        result = front * 255 / (255 - back) 
        result[result > 255] = 255
        result[back == 255] = 255
        
        return result.astype('uint8')

    def grayscale(rgb):
        
        return numpy.dot(rgb[...,:3], [0.299, 0.587, 0.114])
  
    s = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    
    g = grayscale(s)
    i = 255 - g
  
    b = scipy.ndimage.filters.gaussian_filter(i, sigma = 10)
    
    r = dodge(b, g)

    img = PIL.Image.fromarray(r)
    #cv2.imwrite('output/img-sketch.jpg', r)

    #data = io.BytesIO()
    #img.save(data, "JPEG")
    #encoded_img_data = base64.b64encode(data.getvalue())

    #my_str = encoded_img_data.decode('utf-8')
    #return my_str
    return img



def generate_image1(text):

    response = openai.Image.create(prompt=text, n=1, size="1024x1024")

    image_url = response['data'][0]['url']

    img = Image.open(requests.get(image_url, stream=True).raw)

    #img.save('img.jpg')

    return img
#######################################################################################
#applying filters to the image

#Brightness
def brightness_control(image_path,brightness):
  brightness = int(((brightness + 127)*(127 + 127)/(100 + 100)) - 127)
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  if brightness > 0:
      shadow = brightness
      highlight = 255
  else:
      shadow = 0
      highlight = 255 + brightness
  alpha_b = (highlight - shadow)/255
  gamma_b = shadow
  
  image = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
  #cv2_imshow(image)
  cv2.imwrite('temp.jpg',image)

#Contrast
def contrast_control(image_path, contrast):
  contrast = int(((contrast + 64)*(64 + 64)/(100 + 100)) - 64)
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  if contrast != 0:
    f = 131*(contrast + 127)/(127*(131-contrast))
    alpha_c = f
    gamma_c = 127*(1-f)
    
    image = cv2.addWeighted(image, alpha_c, image, 0, gamma_c)
  #cv2_imshow(image)
  cv2.imwrite('temp.jpg',image)

#Saturation
def saturation_control(image_path,value):
  value = 1 + (value/100)
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  hsvImg = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
  hsvImg[...,1] = hsvImg[...,1]*value
  image=cv2.cvtColor(hsvImg,cv2.COLOR_HSV2BGR)
  #cv2_imshow(image)
  cv2.imwrite('temp.jpg',image)

#Sharpness
def sharpen_control(image_path, amount):
  amount = int(((amount - 1)*(3 - 1)/(100 - 0)) + 1)
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  kernel_size=(5, 5)
  sigma=1.0 
  threshold=0
  blurred = cv2.GaussianBlur(image, kernel_size, sigma)
  sharpened = float(amount + 1) * image - float(amount) * blurred
  sharpened = numpy.maximum(sharpened, numpy.zeros(sharpened.shape))
  sharpened = numpy.minimum(sharpened, 255 * numpy.ones(sharpened.shape))
  sharpened = sharpened.round().astype(numpy.uint8)
  if threshold > 0:
      low_contrast_mask = numpy.absolute(image - blurred) < threshold
      numpy.copyto(sharpened, image, where=low_contrast_mask)
  #cv2_imshow(sharpened)
  cv2.imwrite('temp.jpg',sharpened)

#Hue
def hue_control(image_path,value):
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
  h, s, v = cv2.split(hsv)
  h += value
  final_hsv = cv2.merge((h, s, v))
  image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
  #cv2_imshow(image)
  cv2.imwrite('temp.jpg',image)

#Vignette
def vignette_control(image_path,vignette):
  vignette = int(175.00/((vignette)/(100.00)))
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  rows,cols = image.shape[:2]
  zeros = numpy.copy(image)
  zeros[:,:,:] = 0
  a = cv2.getGaussianKernel(cols,vignette)
  b = cv2.getGaussianKernel(rows,vignette)
  c = b*a.T
  d = c/c.max()
  zeros[:,:,0] = image[:,:,0]*d
  zeros[:,:,1] = image[:,:,1]*d
  zeros[:,:,2] = image[:,:,2]*d
  #cv2_imshow(zeros)
  cv2.imwrite('temp.jpg',zeros)

#Cartoon
def cartoon_effect(image_path):
  img_rgb = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  num_down = 2
  num_bilateral = 7
  img_color = img_rgb
  for _ in range(num_down):
    img_color = cv2.pyrDown(img_color)
  for _ in range(num_bilateral):
    img_color = cv2.bilateralFilter(img_color, d=9, sigmaColor=9, sigmaSpace=7)
  for _ in range(num_down):
    img_color = cv2.pyrUp(img_color)
  img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
  img_blur = cv2.medianBlur(img_gray, 7)

  img_edge = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,
                                  blockSize=9, C=2)
  img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
  img_cartoon = cv2.bitwise_and(img_color, img_edge)
  #cv2_imshow(img_cartoon)
  cv2.imwrite('temp.jpg',img_cartoon)

#Blur
def blur_filter(image_path):
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  image = cv2.GaussianBlur(image,(5,5),cv2.BORDER_DEFAULT)
  #cv2_imshow(image)
  cv2.imwrite('temp.jpg',image)

#Edge
def edge_filter(image_path):
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  image = cv2.Canny(image,100,300)
  #cv2_imshow(image)
  cv2.imwrite('temp.jpg',image)

#Vintage
def vintage_filter(image_path):
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  rows, cols = image.shape[:2]
  # Create a Gaussian filter
  kernel_x = cv2.getGaussianKernel(cols,200)
  kernel_y = cv2.getGaussianKernel(rows,200)
  kernel = kernel_y * kernel_x.T
  filter = 255 * kernel / numpy.linalg.norm(kernel)
  vintage_im = numpy.copy(image)
  # for each channel in the input image, we will apply the above filter
  for i in range(3):
      vintage_im[:,:,i] = vintage_im[:,:,i] * filter
  #cv2_imshow(vintage_im)
  cv2.imwrite('temp.jpg',vintage_im)

#Black and White
def blackwhite_filter(image_path):
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  #cv2_imshow(image)
  cv2.imwrite('temp.jpg',image)

#Monochrome
def monochrome_filter(image_path):
  image = cv2.cvtColor(numpy.array(image_path), cv2.COLOR_RGB2BGR)
  (thresh, im_bw) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  #cv2_imshow(im_bw)
  cv2.imwrite('temp.jpg',im_bw)

#Main Function
def photoEditor(imageInput, brightnessValue, contrastValue, saturationValue, hueValue, vignetteValue, sharpenValue, effectList):
  #image_inp = Image.fromarray(imageInput)
  #image_inp.save("temp.jpg") 

  image = cv2.cvtColor(numpy.array(imageInput), cv2.COLOR_RGB2BGR)
  image = cv2.resize(image,(800,800))
  cv2.imwrite('temp.jpg', image)

  if brightnessValue != 0.00:
    brightness_control('temp.jpg',brightnessValue)

  if contrastValue != 0.00:
    contrast_control('temp.jpg',contrastValue)

  if saturationValue != 0.00:
    saturation_control('temp.jpg',saturationValue)

  if hueValue != 0.00:
    hue_control('temp.jpg',hueValue)

  if vignetteValue != 0.00:
    vignette_control('temp.jpg',vignetteValue)
    
  if sharpenValue != 0.00:
    sharpen_control('temp.jpg',sharpenValue)

  if len(effectList) != 0:
    if 'Cartoon' in effectList:
      cartoon_effect('temp.jpg')

    if 'Edge' in effectList:
      edge_filter('temp.jpg')

    if 'Vintage' in effectList:
      vintage_filter('temp.jpg')

    if 'Blur' in effectList:
      blur_filter('temp.jpg')

    if 'Black & White' in effectList:
      blackwhite_filter('temp.jpg')

    if 'Monochrome' in effectList:
      monochrome_filter('temp.jpg')

  im = Image.open('temp.jpg')
  data = io.BytesIO()
  im.save(data, "JPEG")
  encoded_img_data = base64.b64encode(data.getvalue())
  my_str = encoded_img_data.decode('utf-8')
  return my_str
#######################################################################################


#######################################################################################
#Replicate.com 
#1) Restore Image
#app = replicate.Client(api_token="r8_XSxDOhlH9rJYRVskdoMjqxmIfKkZYUP1vgnWy")

os.environ["REPLICATE_API_TOKEN"] = "r8_XSxDOhlH9rJYRVskdoMjqxmIfKkZYUP1vgnWy"

def restore_image(image):
  image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
  print(image)
  output = replicate.run(
    "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
    input={"image": image}
  )
  return output
