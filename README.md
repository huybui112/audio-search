# audio-search

#cài đặt thư viện
pip install fastapi uvicorn fastdtw numpy

#Chạy server
uvicorn main:app --reload

#API upload (1 file) - POST
http://127.0.0.1:8000/upload-audio/

![image](https://github.com/user-attachments/assets/a3f58dd6-b506-44b3-b5f7-9541a9615eee)



#API upload (nhiều file) - POST
http://127.0.0.1:8000/upload-multiple-audio/?directory_path=D:\test audio

#API get - GET
http://127.0.0.1:8000/get-audio/CuocDoiVanDepSao (mp3cut.net).wav

#API search
http://127.0.0.1:8000/search-audio/
