
from django.shortcuts import redirect, render
from.models import reg,normal,xray
import cv2
import numpy as np
from django.shortcuts import render
import base64

from tensorflow.keras.models import load_model # type: ignore
from django.http import HttpResponse
from django.contrib.auth import logout

image_path=''
predictions=''
from tensorflow.keras.models import load_model # type: ignore

try:
    model = load_model('model.h5')
except Exception as e:
    pass
   

# Create your views here.
def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        a=request.POST.get('name')
        b=request.POST.get('age')
        c=request.POST.get('uname')
        d=request.POST.get('email')
        e=request.POST.get('phone')
        f=request.POST.get('password')
        g=request.POST.get('cpassword')
        h=request.POST.get('gender')
        reg(name=a,age=b,uname=c,email=d,phone=e,password=f,cpassword=g,gender=h).save()
        return render(request,'index.html')
    else:
        return render(request,'register.html')
    
def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        # print(name)
        password = request.POST.get('password')
        # print('joy')
        cr = reg.objects.filter(email=email,password=password)
        if cr:
            userd =reg.objects.get(email=email,password=password)
            id=userd.id
            email=userd.email
            password=userd.password
            request.session['email']=email
            return render(request,'home.html')
        else:
            
            return render(request,'login.html')
    else:
        return render(request,'login.html')
    
def home(request):
    return render(request,'home.html')

def logoutv(request):
    logout(request)
    return redirect(index)

def profile(request):
    email=request.session['email']
    cr=reg.objects.get(email=email)
    if cr:
        user_info={
            'uname':cr.uname,
            'name':cr.name,
            'phone':cr.phone,
            'age':cr.age,
            'email':cr.email,
            'password':cr.password,
            'cpassword':cr.cpassword,
            'gender':cr.gender,
            }
        return render(request,'profile.html',user_info)
    else:
        return render(request,'profile.html')

def proupdate(request):
    email=request.session['email']
    if request.method == "POST":
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password=request.POST.get('password') 
        cpassword=request.POST.get('cpassword') 
        name=request.POST.get('name') 
        phone=request.POST.get('phone') 
        age=request.POST.get('age') 
        gender=request.POST.get('gender')
        dt=reg.objects.get(email=email)
        dt.name=name
        dt.uname=uname
        dt.email=email
        dt.password=password
        dt.cpassword=cpassword
        dt.phone=phone
        dt.age=age
        dt.gender=gender
        dt.save()
        response=redirect('/profile/')
        return response
        # return render(request,'profile.html')
    else:
        return render(request,'profile.html')



def checkdisease(request):
    if request.method == 'POST':
        img1 = request.FILES.get('img1')
        # Save the uploaded image
        normal_img = normal(img=img1)
        normal_img.save()

        # Read the uploaded image
        image_path = normal_img.img.path
        img = cv2.imread(image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Thresholding to identify black regions
        ret, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)

        # Invert the binary image
        thresh = cv2.bitwise_not(thresh)

        # Find contours in the binary image
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw bounding boxes around black spots
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert the image to base64 string for displaying in HTML
            _, buffer = cv2.imencode('.jpg', img)
            segmented_img = base64.b64encode(buffer).decode('utf-8')

        # Pass the processed image to the HTML page to display
        return render(request, 'result.html', {'image': segmented_img})

    return render(request, 'fileupload.html')



def xrayupload(request):
    xray1 = ''
    if request.method == 'POST':
        xrayimg = request.FILES.get('xrayimg')
        # Assuming you have a model named XRay to save the uploaded image
        xray1 = xray(ximg=xrayimg)
        xray1.save()

        # Perform watershed segmentation
        xray_path = xray1.ximg.path
        print('path is', xray_path)
        
        # Ensure xray_path is valid
        if xray_path:
            # Read the image
            img = cv2.imread(xray_path)
            
            # Convert image to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            damage_score=load_unet()
            
       
            ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
            
        
            area = np.sum(thresh == 255)
            
      
            damage_score = area / (img.shape[0] * img.shape[1])  # Normalize area by image size


            if damage_score == 0:
                with open(xray_path, "rb") as f:
                    original_img = f.read()
                return HttpResponse(original_img, content_type="image/jpeg")
            else:
                            # Compute the center of the image
                center_x = img.shape[1] // 2
                center_y = img.shape[0] // 2
            
            # Calculate the bounding box coordinates
                box_width = 100  # Adjust the width of the bounding box as needed
                box_height = 100  # Adjust the height of the bounding box as needed
                x = max(0, center_x - box_width // 2)
                y = max(0, center_y - box_height // 2)
                x_end = min(img.shape[1], center_x + box_width // 2)
                y_end = min(img.shape[0], center_y + box_height // 2)
            
            # Draw a bounding box from the center of the image
                cv2.rectangle(img, (x, y), (x_end, y_end), (0, 255, 0), 2)


            # If damage_score is non-zero, render the segmented image
            _, buffer = cv2.imencode('.jpg', img)
            segmented_img = base64.b64encode(buffer).decode('utf-8')
            return render(request, 'segmented_xray.html', {'segmented_img': segmented_img, 'damage_score': damage_score})
        else:
            return HttpResponse("Error: Segmentation failed. Could not find image path.")

    else:
        return render(request, 'xray.html')



def load_unet():
    # Load and preprocess the image
    predictions=''
    # Make predictions
    try:
        predictions = model.predict(image_path)
    except Exception as e:

        pass

    return predictions
