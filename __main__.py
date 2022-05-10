import AudioSet
import constants
import glob

def main():

    DIR = "Speaking_Dataset"

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

    aud = AudioSet.AudioSet(csv="AudioSet Data\\balanced_train_segments.csv", dir=DIR, ydl_opts = config)
    print(aud.df.head(100))
    aud.filter(id="/m/05zppz")
    print(aud.df.size)

    aud.download_full_vids()

    for file in list(glob.glob(f'{DIR}}\\Full\\*.wav')):
        aud.splice_audio(file)





if __name__ == '__main__':
    main()
