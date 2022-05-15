import AudioSet
import constants
import glob

def main():

    DIR = "Snoring_Dataset"

    config = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
        'outtmpl': 'Speaking_Dataset\\Full\\%(id)s.%(ext)s'
    }

    aud = AudioSet.AudioSet(dir=DIR)
    print(aud.df.head())
    # aud.filter(id="/m/05zppz")
    # print("\n\n\n\n")
    # print(aud.df.head(5))
    #
    # aud.download()
    #
    for file in list(glob.glob('Snoring_Dataset\\Clips\\further splice\\*.wav')):
        aud.chunkify(wav=file, seconds=1)





if __name__ == '__main__':
    main()
