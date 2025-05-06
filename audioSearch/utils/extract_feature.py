import librosa
import numpy as np

# def extract_mfcc(file_path, n_mfcc=13):
#     y, sr = librosa.load(file_path, sr=None)
#     mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
#     return mfcc.mean(axis=1)  # Trung bình theo thời gian

def extract_mfcc(file_path, n_mfcc=13, hop_length=512, n_fft=2048, normalize=True):
    try:
        # Tải file âm thanh
        y, sr = librosa.load(file_path, sr=None)
        
        # Chuẩn hóa tín hiệu
        y = y / np.max(np.abs(y)) if np.max(np.abs(y)) != 0 else y

        # Trích xuất MFCC
        mfcc = librosa.feature.mfcc(
            y=y, 
            sr=sr, 
            n_mfcc=n_mfcc, 
            hop_length=hop_length,  # Khoảng cách giữa các khung
            n_fft=n_fft  # Kích thước FFT
        )

        # Chuẩn hóa MFCC (optional)
        if normalize:
            mfcc = (mfcc - np.mean(mfcc)) / np.std(mfcc)

        # Lấy trung bình theo thời gian
        mfcc_mean = mfcc.mean(axis=1)
        return mfcc_mean

    except Exception as e:
        raise Exception(f"Không thể trích xuất MFCC từ {file_path}: {str(e)}")