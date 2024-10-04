# =============================================================================
# MEMASUKAN DEPENDENCY 
# =============================================================================

from ultralytics import YOLO
import numpy as np
import cv2 as cv


# =============================================================================
# MEMBUAT KELAS PEOPLE COUNTER 
# =============================================================================

class peopleCounter:
# =============================================================================
#     DEFINISI ATRIBUT YANG DIPERHATIKAN
# =============================================================================
    def __init__(self,cameraPov,file=None,nPeople=18):
        self.cameraPov=cameraPov #USER MEMASUKAN APAKAH KAMERA DEKAT, SEDANG ATAU JAUH
        self.file=file #NAMA FILE
        self.model=None #MODELTERPILIH
        self.frame=None #FRAME VIDEO
        self.nPeople=nPeople #BATAS WARNING (BANYAK ORANG)
    
# =============================================================================
#     MEMILIH MODEL YANG SESUAI DENGAN CAMERAPOV 
# =============================================================================
    def chooseModel(self):
        if self.cameraPov=="Close": #MODEL CLOSE
            self.model=YOLO("yolo11x.pt")
        elif self.cameraPov=="Medium" and self.file!=None: #MODEL MEDIUM
            self.model=YOLO(r"D:\Setelah Kuliah\Lamaran Pekerjaan\Kecilin\People Counter\CountingPeople2-20241003T143211Z-001\CountingPeople2\drive-download-20241003T152014Z-001\runs\detect\train\weights\best.pt")
        elif self.cameraPov=="Far" and self.file!=None: #MODEL FAR
            self.model=YOLO(r"D:\Setelah Kuliah\Lamaran Pekerjaan\Kecilin\People Counter\CountingPeople-20241003T055857Z-001\CountingPeople\runs\detect\train4-20241003T072629Z-001\train4\weights\best.pt")
        else:
            print("COBA LAGI LAINYA")
            
# =============================================================================
#     METHOD MENGHITUNG BANYAK ORANG DALAM FRAME
# =============================================================================
    def calcPeople(self,results, frame,nPeople):
        nBoxes=0 #INISIALISASI BANYAK ORANG
        
        #AREA WARNING
        area=np.array([(int(self.frame.shape[1]/4),0),
                   (int(self.frame.shape[1]*3/4),0),
                   (int(self.frame.shape[1]*3/4),self.frame.shape[0]),
                   (int(self.frame.shape[1]/4),self.frame.shape[0])],np.int32)
        
        #MENGGAMBAR AREA WARNING
        cv.polylines(frame, [area], True,(255,0,0),2)
        #MEMULAI PERHITUNGAN
        for result in results:
            boxes=result.boxes.xyxy #MENDAPATKAN NILAI X,Y,X1,Y1
        for box in boxes:
            x,y,x1,y1=box
            x=int(x)
            y=int(y)
            x1=int(x1)
            y1=int(y1)
            #MENDAPATKAN NILAI TENGAH DARI BOX
            cx=int(x+x1)//2 
            cy=int(y+y1)//2
            # CEK APAKAH TERMASUK DALAM AREA
            hasil=cv.pointPolygonTest(area,((cx,cy)),False)
            # MENGGAMBAR CIRCLE PADA ORANG
            if hasil>=0:
                cv.circle(frame,(cx,cy),4,(255,0,0),-1)
                nBoxes+=1
        if nBoxes>=nPeople:
            color=(0,0,255)
        else:
            color=(255,0,0)
        cv.putText(frame, "{}".format(nBoxes), 
                   (int((frame.shape[0])/2-180),int((frame.shape[1])/2-180)), 
                   cv.FONT_HERSHEY_SIMPLEX, 2, color, 10)
        
# =============================================================================
#       MEREKAM VIDEO DAN MENGHITUNG
# =============================================================================
    def forVideo(self,choosenPov):
        cap=cv.VideoCapture(choosenPov)
        while True:
            success, self.frame = cap.read()
            if not success:
                break
            key=cv.waitKey(1)
            results=self.model.track(self.frame,verbose=False,conf=0.1)
            self.calcPeople(results,self.frame,self.nPeople)
            cv.imshow("Counting Result",self.frame)
            if key==27:
                break
        cap.release()
        cv.destroyAllWindows()
    
# =============================================================================
#       MENDAPATKAN ARRAY IMAGE DAN MENGHITUNG
# =============================================================================
    def forImage(self,choosenPov):
        self.frame=cv.imread(choosenPov)
        while True:
            result=self.model.track(self.frame,verbose=False,conf=0.1)
            self.calcPeople(result,self.frame,self.nPeople)
            cv.imshow("Counting Result",self.frame)
            key=cv.waitKey(1)
            if key==27:
                break
        cv.destroyAllWindows()
    
# =============================================================================
#       MENGHITUNG BERDASARKAN INPUT
# =============================================================================
    def counting(self):
        # CEK APAKAH TERDAPAT FILE
        if (isinstance(self.file,str))==True:
            choosenPov=self.file
            _,form=choosenPov.split(".")
            if form=="mp4": #CEK APAKAH VIDEO
                self.forVideo(choosenPov)
            elif form=="jpg" or form=="png": #CEK APAKAH GAMBAR
                self.forImage(choosenPov)
            else:
                print("GAGAL INPUT")
        else:
            choosenPov=0
            self.forVideo(choosenPov)
        