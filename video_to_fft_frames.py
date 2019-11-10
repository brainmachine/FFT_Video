"""
Load a video, convert each frame to a 2D Spectrogram and export image
Run this first, then use combine_frames.py to create a video.
"""
import os
import multiprocessing as mp
import cv2
import numpy as np
import ffmpeg

mp.set_start_method('spawn', True)

class FrameConverter:
    """ Convert video to 2D DFT frames """

    def __init__(self, input_path):
        self.input_path = input_path
        self.width, self.height = self._get_size()
        self.num_chans = 3 # RGB, TODO: Handle monochrome and RGBA videos

        self.fileinfo = ffmpeg.probe(input_path)
        self.pix_fmt = self._get_pix_fmt()

        self.video = self._load_video()
        self.export_path = None

        self._create_export_path(input_path)

    def _get_size(self):
        """ Find the width and height of the video. """
        # TODO: Automatically pick the right stream
        width = self.fileinfo['streams'][1]['width']
        height = self.fileinfo['streams'][1]['height']

        return [width, height]

    def _get_pix_fmt(self):
        return self.fileinfo['streams'][1]['pix_fmt']

    def _get_fps(self):
        """ Find the FPS of the video, some magic involved...
        Maybe there's a better way to do this. """
        # Split the string and calculate the fps
        a, b = self.fileinfo['streams'][1]['avg_frame_rate'].split('/')
        a, b = float(a), float(b)
        fps = a/b
        return fps

    def _create_export_path(self, input_path):
        """ Create an export folder if it doesn't exist already. """
        _, file_name = os.path.split(input_path)

        # drop the extension
        file_name, _ = os.path.splitext(file_name)
        self.export_path = 'output/%s'%file_name
        if not os.path.exists(self.export_path):
            os.mkdir(self.export_path)
            print("Created path --> %s"%input_path)

    def _load_video(self):
        # Load the video
        # TODO: "deprecated pixel format used, make sure you did set range correctly"
        # https://stackoverflow.com/questions/23067722/swscaler-warning-deprecated-pixel-format-used

        out, _ = (
            ffmpeg
            .input(self.input_path)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .run(capture_stdout=True, capture_stderr=True)

        )
        # Convert to Numpy Array
        video = (
            np
            .frombuffer(out, np.uint8)
            .reshape([-1, self.height, self.width, 1])
        )

        return video

    def convert_video_to_images(self, video, offset):
        """ Iterate through all the video frames and export as PNGs.
            We pass in a video segment + the frame offset so we can support multiprocessing.
        """
        for i, frame in enumerate(video):
            print("converting frame to fft")
            frame = np.fft.fft2(frame)
            fshift = np.fft.fftshift(frame)
            # TODO: Deal with divide-by-zero
            magnitude_spectrum = 20*np.log(np.abs(fshift))

            # Normalize magnitude_spectrum
            magnitude_spectrum = magnitude_spectrum/magnitude_spectrum.max()*255.0
            magnitude_spectrum.max()

            # Save the image
            _, filename = os.path.split(self.input_path)
            filename, _ = os.path.splitext(filename)
            outfile_path = 'output/%s/%s_fft_%s.png'% (filename, filename, str(i+offset).zfill(3))
            print(outfile_path)
            cv2.imwrite(outfile_path, magnitude_spectrum)
