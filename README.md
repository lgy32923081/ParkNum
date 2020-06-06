# ParkNum
it help you When you park your car. (Used Yolo, Ocr etc...)

#오류 해결

1.error(2)가 뜬다면 File - setting - Project : parkNum - Project Interpreter - (venv) 설정

#환경 설정 

1.google vision api

cmd 명령어사용 : setx GOOGLE_APPLICATION_CREDENTIALS (json 파일 위치)(json 파일 이름).json
pip install google

2.darkflow

## install
pip install tensorflow==1.14.0
pip install opencv-python (4.2.0.32)
pip install cython (0.29.15)

##repo download
python setup.py build_ext --inplace
python flow --h

##start
pip install .

##edit
darkflow\darkflow\net\yolo\misc.py 수정
 parkingLabel = ["parknum"] 추가
 park_models =['parking-yolo-obj'] 추가

 def labels(meta,FLAGS)에  
 elif model in park_models: print("Model has a park model name, loading park labels.") 
  file = os.path.join(FLAGS.config,park_names) with open(file, 'r') as f: meta['labels'] = list() labs = [l.strip() for l in f.readlines()] for lab in labs: if lab == '----': break meta['labels'] += [lab] if len(meta['labels']) == 0: meta['labels'] = labels20 else: meta['labels'] = parkingLabel
 추가

3.firebase

##install
pip install firebase_admin
pip install pirebase -> if error of setup.py occured, click this url 
https://m.blog.naver.com/vvv1ct0r/220930787642


#참고링크

google api : https://ssungkang.tistory.com/m/entry/Google-Vision-API-%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%9C-%EA%B8%80%EC%9E%90-%EC%9D%B8%EC%8B%9D

darkflow : https://junyoung-jamong.github.io/deep/learning/2019/01/22/Darkflow%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%B4-YOLO%EB%AA%A8%EB%8D%B8-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EB%94%94%ED%85%8D%EC%85%98-%EA%B5%AC%ED%98%84-in-windows.html

firebase : https://romeoh.tistory.com/entry/Firebase-Python-Firebase-Realtime-Database
