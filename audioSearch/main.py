from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from db.audio_files_db import create_audio_file_db, insert_audio_file, get_audio_file
from db.audio_features_db import create_audio_feature_db, insert_audio_feature, get_all_features
from utils.extract_feature import extract_mfcc
import numpy as np
from tempfile import NamedTemporaryFile
from fastapi import FastAPI, HTTPException, Response
from fastdtw import fastdtw

app = FastAPI()

# Tạo database khi app khởi động
create_audio_file_db()
create_audio_feature_db()

@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.wav'):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file WAV.")

    filename = file.filename
    contents = await file.read()

    try:
        insert_audio_file(filename, contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu file vào DB: {e}")

    temp_path = None
    try:
        with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        mfcc = extract_mfcc(temp_path)
        insert_audio_feature(filename, mfcc)
    except Exception as e:
        print(f"Lỗi MFCC: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi trích xuất MFCC: {e}")
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

    return {"message": f"Đã lưu file {filename} và đặc trưng MFCC thành công."}

@app.get("/get-audio/{filename}")
async def get_audio(filename: str):
    data = get_audio_file(filename)
    if data is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy file")

    # Trả về dữ liệu nhị phân trực tiếp
    return Response(
        content=data,
        media_type="audio/wav",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/search-audio/")
async def search_audio(file: UploadFile = File(...)):
    # Đọc file và trích MFCC
    contents = await file.read()
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        temp_file.write(contents)
        temp_path = temp_file.name

    try:
        query_mfcc = extract_mfcc(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi trích MFCC: {e}")
    finally:
        os.remove(temp_path)

    # So sánh với MFCC trong database
    all_features = get_all_features()
    results = []
    THRESHOLD = 10.0  # Ngưỡng khoảng cách
    for fname, mfcc_vec in all_features:
        # distance = np.linalg.norm(mfcc_vec - query_mfcc)
        distance, _ = fastdtw(query_mfcc.T, mfcc_vec.T)
        if distance < THRESHOLD:  
            results.append((fname, float(distance)))

    if not results:
        return {"message": "Không tìm thấy file nào tương tự."}

    results.sort(key=lambda x: x[1])
    top_matches = [{"filename": r[0], "distance": r[1]} for r in results[:5]]
    return {"top_matches": top_matches}


@app.post("/upload-multiple-audio/")
async def upload_multiple_audio(directory_path: str):
    # Kiểm tra thư mục có tồn tại không
    if not os.path.isdir(directory_path):
        raise HTTPException(status_code=400, detail="Thư mục không tồn tại.")

    results = []
    for filename in os.listdir(directory_path):
        # Chỉ xử lý file WAV
        if not filename.lower().endswith('.wav'):
            continue

        file_path = os.path.join(directory_path, filename)
        try:
            # Đọc file
            with open(file_path, "rb") as f:
                contents = f.read()

            # Lưu vào DB
            insert_audio_file(filename, contents)

            # Trích xuất MFCC
            temp_path = None
            try:
                with NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    temp_file.write(contents)
                    temp_path = temp_file.name

                mfcc = extract_mfcc(temp_path)
                insert_audio_feature(filename, mfcc)
                results.append({"filename": filename, "status": "Thành công"})
            except Exception as e:
                results.append({"filename": filename, "status": f"Lỗi trích MFCC: {str(e)}"})
            finally:
                if temp_path and os.path.exists(temp_path):
                    os.remove(temp_path)

        except Exception as e:
            results.append({"filename": filename, "status": f"Lỗi lưu file: {str(e)}"})

    if not results:
        raise HTTPException(status_code=400, detail="Không tìm thấy file WAV nào trong thư mục.")

    return {"results": results}