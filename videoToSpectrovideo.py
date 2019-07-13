# from PIL import Image

import cv2
import numpy as np
from matplotlib import pyplot as plt
import ffmpeg

# Load a video for conversion
# in_file = ffmpeg.input('input/split_waves.mp4')

width = 1920
height = 1080

out, _ = (
    ffmpeg
    .input('input/split_waves_short.mp4')
    .output('pipe:', format='rawvideo', pix_fmt='gray')
    .run(capture_stdout=True)
)
video = (
    np
    .frombuffer(out, np.uint8)
    .reshape([-1, height, width, 1])
)

print("\n \n ------------------------------------- \n \n")
print("video.shape (ndarray) --> " + str(video.shape))

for i, frame in enumerate(video):
    print("converting frame to fft")
    f = np.fft.fft2(frame)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    
    # Normalize magnitude_spectrum
    magnitude_spectrum = magnitude_spectrum/magnitude_spectrum.max()*255.0
    magnitude_spectrum.max()

    # Save the image
    outfile_path = 'output/fft_video_frames/split_wave_short_fft_%s.png'%str(i).zfill(3)
    cv2.imwrite(outfile_path, magnitude_spectrum)


# Using NumPy
# This saves out a good looking PNG at the end

# img = cv2.imread('input/A-Consensus.tif', cv2.IMREAD_GRAYSCALE)
# f = np.fft.fft2(img)
# fshift = np.fft.fftshift(f)
# # magnitude_spectrum = 20*np.log(np.abs(fshift))
# magnitude_spectrum = 20*np.log(np.abs(fshift))


# TODO: Try mapping the fshift from min() to max() making it 0-255, not the abs pipmethod (not backwards compatible)
#magnitude_spectrum = np.asarray(magnitude_spectrum, dtype=np.float32)

