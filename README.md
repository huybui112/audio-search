# audio-search

#cài đặt thư viện
pip install fastapi uvicorn fastdtw numpy

#Cài đặt database Sqlite3

![image](https://github.com/user-attachments/assets/348c2a8e-9663-4d80-9213-87094767b302)

#Chạy server
uvicorn main:app --reload

#API upload (1 file) - POST
http://127.0.0.1:8000/upload-audio/

![image](https://github.com/user-attachments/assets/a3f58dd6-b506-44b3-b5f7-9541a9615eee)


#API upload (nhiều file) - POST
http://127.0.0.1:8000/upload-multiple-audio/?directory_path=D:\test audio

![image](https://github.com/user-attachments/assets/fed14043-fc84-4144-92d3-dfe51c017dae)


#API get - GET
http://127.0.0.1:8000/get-audio/CuocDoiVanDepSao (mp3cut.net).wav

![image](https://github.com/user-attachments/assets/4580527e-8c79-4cce-9d43-84428b4126b6)


#API search
http://127.0.0.1:8000/search-audio/

![image](https://github.com/user-attachments/assets/1a03fdbf-3eab-4eec-b81f-76abef8af053)

