from google.cloud import storage
import firebase_admin
from firebase_admin import credentials, storage

import pyrebase


def main():
    cred=credentials.Certificate(r'C:/VisionAPI/projectFirebase.json'.replace('\u202a',""))
    firebase_admin.initialize_app(cred,{
    'storageBucket': 'parking-76066.appspot.com'
    })

    config = {
        "apiKey": "AIzaSyD8frsIPC5o2RMec3To5YkuU6FMrnWGCTI",
        "authDomain": "parking-76066.firebaseapp.com",
        "databaseURL": "https://parking-76066.firebaseio.com",
        "projectId": "parking-76066",
        "storageBucket": "parking-76066.appspot.com",
        "messagingSenderId": "341130119386",
        "appId": "1:341130119386:web:3d2d28e2d9e8acf21ffde3",
        "measurementId": "G-GF6TX0KFFB"
    }
    try:
        f = [open('C:/HC/afterCrop/ocr%d.text'.replace('\u202a',"")%i,'r',encoding='UTF-8')for i in range(1,4)]
        read = []
        for i in range(0,len(f)):
            read.append(f[i].read())
    finally:
        for fh in f:
            fh.close()
    ocr_txt = ""
    for i in range(0,len(read)):
        if(read[i]=="parknum is not found"):
            ocr_txt="null"
        else:
            ocr_txt=read[i]
            break

    print(ocr_txt)

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    db.child("name").child("-M9m61HQdmKX694wJKnF").update({"parknum":ocr_txt})
    # db.child("name").child("-M7qEiKlHjou_PAqcwnt").update({"parknum":ocr_txt})
    print("FireBase에 텍스트를 Update 했습니다.")
    #db.child("name").remove()
    #db = firestore.client()
    bucket = storage.bucket()
    blobs=[]
    for i in range(0,3):
        blobs.append(bucket.blob('Parking{}'.format(i+1)))
    for i in range(0,3):
        outfile = 'C:\\HC\\imgList\\CarLocationImg_{}.jpg'.format(i+1).replace('\u202a',"")
        with open(outfile,'rb') as my_file:
            blobs[i].upload_from_file(my_file)
    print("FireBase storage에 이미지 파일을 저장했습니다.")

# main()
