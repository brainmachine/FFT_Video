import numpy as np

class FrameSplicer:

    def __init__():
        pass

    

    def composite_video(self):
        """ Loads all PNGs from a path and produces a video. """

        # Read the PNGs from here
        images_path = 'output/%s/*.png'%input_filename
        # Save the composite video here
        video_save_path = '%s_fft.%s'%(input_filename, extension)
        print("exporting " + video_save_path)
        (
            ffmpeg
            .input(images_path, pattern_type='glob', framerate=fps)
            .output(video_save_path, format='mp4')
            .run()
        )
        print("saved " + video_save_path)