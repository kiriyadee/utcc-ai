import cv2
from cv2 import imshow
from IPython.display import clear_output

# เปิดวิดีโอ
vid = cv2.VideoCapture("./car-detection.mp4")
try:
    while True:
        # อ่านแต่ละเฟรม
        ret, frame = vid.read()
        if not ret:
            # ปิดการใช้งานวิดีโอหากอ่านเฟรมไม่ได้
            vid.release()
            print('Released Video Resource')
            break
        # แปลงภาพจาก BGR เป็น RGB เพื่อแสดงผลใน Colab
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # แสดงภาพ
        imshow(frame)
        
        # ทำความสะอาดหน้าจอเพื่อแสดงเฟรมใหม่
        clear_output(wait=True)

except KeyboardInterrupt:
    # ปิดการใช้งานวิดีโอเมื่อหยุดการทำงานด้วยคีย์บอร์ด
    vid.release()
    print('Released Video Resource')