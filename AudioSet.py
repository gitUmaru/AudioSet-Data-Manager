from youtube_dl import YoutubeDL
import pandas as pd
import os
import pydub
import numpy as np
from pathlib import Path
import constants
import re

class AudioSet:
    def __init__(self, csv, dir, ydl_opts = {'format': 'bestaudio'}):
        self.csv = csv
        self.dir = dir
        self.ydl_opts = ydl_opts
        self.df = self.make_new()

    def make_new(self):
        rows = []
        frame_header = ["positive_labels", "end_seconds", "start_seconds", "YTID", ""]
        with open(self.csv, 'r') as f_input:
            for row in f_input:
                cols = [col[::-1] for col in row[::-1][2:].split(' ') if len(col)]
                rows.append(cols[:4] + [' '.join(cols[4:][::-1])])

        df = pd.DataFrame(rows, columns=frame_header)
        df.drop(df.columns[len(df.columns)-1], axis=1, inplace=True)
        df = df[df.columns[::-1]]
        df['start_seconds'] = df['start_seconds'].replace(',','',regex=True).astype(float)
        df['end_seconds'] = df['end_seconds'].replace(',','',regex=True).astype(float)
        self.df = df

        return df

    def filter(self, id):
        for index, row in self.df.iterrows():
            if(id not in row["positive_labels"]):
                self.df.drop(index, inplace=True)

        return self.df

    def splice_audio(self, wav, theta=-35):
        sound_file = pydub.AudioSegment.from_wav(wav)

        file = os.path.basename(wav).replace(".wav","")

        annot = self.df[(self.df["YTID"].str.contains(file, na=False))]

        start_time =  int(annot['start_seconds']) * constants.MILLISECONDS
        end_time = int(annot['end_seconds'])* constants.MILLISECONDS

        audio = sound_file[start_time : end_time]

        chunks = pydub.silence.split_on_silence(
            audio,
            min_silence_len = 500,
            silence_thresh = theta
        )

        for i, chunk in enumerate(chunks):
            silence_chunk = pydub.AudioSegment.silent(duration=500)
            # Add the padding chunk to beginning and end of the entire chunk.
            audio_chunk = silence_chunk + chunk + silence_chunk

            # Normalize the entire chunk.
            normalized_chunk = self.__match_target_amplitude__(audio_chunk, -20.0)

            normalized_chunk.export(f'{self.dir}\\Clips\\{file}_{i}.wav', format="wav")

    def __match_target_amplitude__(self, aChunk, target_dBFS):
        ''' Private function to normalize given audio chunk '''
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)

    def chunkify(self, wav, seconds):
        myaudio =  pydub.AudioSegment.from_file(wav , "wav")
        file = os.path.basename(wav).replace(".wav","")

        chunk_length_ms = seconds*constants.MILLISECONDS
        chunks =  pydub.utils.make_chunks(myaudio, chunk_length_ms)

        for i, chunk in enumerate(chunks):
            chunk.export(f"{self.dir}\\1\\{file}_{i}.wav", format="wav")

    def download_full_vids(self):
        with YoutubeDL(self.ydl_opts) as ydl:
            for index, row in self.df.iterrows():
                print(row["YTID"])
                try:
                    ydl.download([f'https://www.youtube.com/watch?v={row["YTID"]}'])
                except:
                    pass
