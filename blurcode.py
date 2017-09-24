import http.client, urllib, urllib.request, base64, json, copy, array
import tkinter, tkinter.font
import PIL
from PIL import Image, ImageFilter

color = "Deep Sky Blue"

gui = tkinter.Tk()
gui.title("Demotion 1.0")
gui.configure(background=color)

selectedEmo = tkinter.StringVar()
selectedEmo.set('happiness')

def buttonPress(event):
    url = e1.get()
    saveTarget = e2.get()
    LinkorFile = isLink.get()
    if(LinkorFile == 0):
        uploadFile = False
    else:
        uploadFile = True
    if(saveTarget==''):
        saveTarget='DemotionImage.jpg'
    selectedEmotion = selectedEmo.get()


    #setting up the stuff to send to Microsoft
    if(uploadFile==False):
        body = {"url": url}
        body_json = json.dumps(body)
        headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '<subscription_key>',
    }
    else:
        with open(url, "rb") as imageFile:
            f=imageFile.read()
            b=bytearray(f)
            body = b
            body_json = body
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '<subscription_key>',
        }

    params = urllib.parse.urlencode({})

    #send the data to Microsoft and get back the emotions
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body_json, headers)
        response = conn.getresponse()
        data = response.read()
        faces = json.loads(data)
        conn.close()
        
    except Exception as e:
        tkinter.MessageBox.showInfo("something broke", e)

    happyFaces = []
    sadFaces = []
    neutralFaces = []
    contemptFaces = []
    disgustFaces = []
    angryFaces = []
    surpriseFaces = []
    fearFaces = []

    for face in faces:
        if (face['scores']['happiness'] > 0.5):
            happyFaces.append(face['faceRectangle'])
        if (face['scores']['sadness'] > 0.5):
            sadFaces.append(face['faceRectangle'])
        if (face['scores']['neutral'] > 0.5):
            neutralFaces.append(face['faceRectangle'])
        if (face['scores']['contempt'] > 0.5):
            contemptFaces.append(face['faceRectangle'])
        if (face['scores']['disgust'] > 0.5):
            disgustFaces.append(face['faceRectangle'])
        if (face['scores']['anger'] > 0.5):
            angryFaces.append(face['faceRectangle'])
        if (face['scores']['surprise'] > 0.5):
            surpriseFaces.append(face['faceRectangle'])
        if (face['scores']['fear'] > 0.5):
            fearFaces.append(face['faceRectangle'])

    #pick out good and bad faces
    goodFaces = []
    badFaces = []
    for face in faces:
        if(face['scores'][selectedEmotion]>0.5):
            goodFaces.append(face['faceRectangle'])
        else:
            badFaces.append(face['faceRectangle'])

    
    #retrieve and save image if online
    if(uploadFile==False):
        urllib.request.urlretrieve(body['url'],saveTarget)
        im_input  = Image.open(saveTarget)
    else:
        im_input = Image.open(url)
    for face in goodFaces:
        box = (face['left'], face['top'],
               face['left'] + face['width'],
               face['top'] + face['height'])
        crop_image = im_input.crop(box)
        crop_image = crop_image.filter(ImageFilter.GaussianBlur(20))
        im_input.paste(crop_image, box)


    im_input.show()
    #save output image
    im_input.save(saveTarget)



#changes the font size
helv36 = tkinter.font.Font(family='Helvetica', size=24, weight='bold')


#lbl = tkMessageBox.showinfo("Enter the Emotion that you would like to Blur")

#changes the font size
lbl = tkinter.Label(gui, text="Select the Emotion that you would like to Blur:", font=helv36, background = color)
lbl.pack()


helv36 = tkinter.font.Font(family='Helvetica', size=30, weight='bold')
EMOTIONS = [
    	("Happiness", "happiness"),
    	("Sadness", "sadness"),
    	("Contempt", "contempt"),
    	("Neutral", "neutral"),
    	("Disgust", "disgust"),
    	("Anger", "anger"),
    	("Surprise", "surprise"),
    	("Fear", "fear"),
	]
gui.geometry("1000x1000")
#Emotion Selection Radio Buttons
for text, emotion in EMOTIONS:
    	b = tkinter.Radiobutton(gui, text=text, variable=selectedEmo, value=emotion, font=helv36, background = color)
    	b.pack()


helv36 = tkinter.font.Font(family='Helvetica', size=24, weight='bold')

#2nd label
lbl2 = tkinter.Label(gui, text="Enter the Link to your picture", font=helv36, background = color)
lbl2.pack()

isLink = tkinter.IntVar()
chck = tkinter.Checkbutton(gui, text="Would you like to Enter a File Directory on your Computer Instead?", variable = isLink, background = color)
chck.pack()

#Emotion Entry GUI
e1 = tkinter.Entry(gui, font=helv36)
e1.pack()

url = e1.get()

lbl3 = tkinter.Label(gui, text="What do you want your filename to be?", font=helv36, background = color)
lbl3.pack()


e2 = tkinter.Entry(gui, font=helv36)
e2.pack()
saveTarget = e2.get()


#Enter Button
button = tkinter.Button(gui, text="Enter",font=helv36, background = color)
button.pack()

button.bind('<Button-1>', buttonPress)

tkinter.mainloop()
