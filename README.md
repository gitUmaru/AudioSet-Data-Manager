# AudioSet Data Manager

A simple python package for managing the audio data from Google Research's ontology of 632 audio event classes and a collection of 2,084,320 human-labeled 10-second sound clips drawn from YouTube videos.

## Description  

Google Research's AudioSet is a repository of audio events that span a wide range of labels. This python package is here to help you navigate, downlead, and edit the entire repository of audio events in order to easily extract the desired files. Each line in the AudioSet `csv` file format has columns defined by the third header line: `# YTID, start_seconds, end_seconds, positive_labels` . The package is based on this loose temporal `.csv` file format; which looks like this:

|                   |                | # Segments csv created Sun Mar 5 10:54:31 2017 | positive_labels           |
|------------------:|---------------:|-----------------------------------------------:|---------------------------|
| # num_ytids=22160 | num_segs=22160 | num_unique_labels=527                          | num_positive_labels=52882 |
| # YTID            | start_seconds  | end_seconds                                    | positive_labels           |
| --PJHxphWEs       | 30.000         | 40.000                                         | "/m/09x0r,/t/dd00088"     |
| ...               | ...            | ...                                            | ...                       |


**DO NOT ALTER CSV FILE. The python package will automatically format into the following:**

| YTID        | start_seconds | end_seconds | positive_labels     |
|-------------|---------------|-------------|---------------------|
| -0RWZT-miFs | 420.000       | 430.000     | "/m/03v3yw,/m/0k4j" |
| ...         | ...           | ...         | ...                 |

## Getting Started

### Dependencies

* Python v3.x
* FFmpeg
* pydub
* youtubedl
* pandas

### Installing

1. To install the python packages simply run the following commands
  * `pip install requirements.txt`
2. Download the correct FFmpeg packages & executable files depedning on your OS
  * [Link here](https://ffmpeg.org/download.html)
3. Add FFmpeg to PATH

### Executing program

#### Creating Manager
* Instantiate AudioSet Manager by passing in arguments
  * `csv` argument is the file path to the csv downloaded from [this page](https://research.google.com/audioset/download.html)
  * `dir` argument is the file path to the desired directory you want files to be saved to
  * `ydl_opts` argument is the youtubedl configuration format of the downloaded files. [See youtubedl docs](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl) for more information and [this](https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312) for possible field options


```py
from AudioSet import AudioSet
aud = AudioSet(csv=CSV, dir=DIR, ydl_opts = YDL_OPTS)
print(aud.df.head()) # See the top 5 rows
```

#### Filtering by `mid`
* In order to narrow down the dataset by a desired audio event, you can filter the entire dataframe according to the audio event's `mid`. Refer to [onotolgy.json](https://github.com/audioset/ontology/blob/master/ontology.json) for the `mid` dictionary


```py
aud.filter("/m/0dgw9r") # Keep only audio clips that contain "Human Sounds"
print(aud.df.head()) # Will only contain rows with "Human Sounds"
```

#### Downloading Videos and Audio Cutting
* One can download all the **audio** in the manager's dataframe
  * Note, this **saves to project home directory**. Specify desired save directory with `ydl_opts` argument in constructor.

```py
aud.download()
```

There are several options for cutting the audio. The `wav` argument is the path to the desired wav file to cut. These all save the clips under the `DIR` folder.

1. Cutting based on `start_time` and `end_time` from AudioSet csv files
  * Export files of audio from `start_time` to `end_time`
  * `aud.split(wav=WAV_PATH)`
2. Cutting based on method 1 and then further cutting based on silence_chunk
  * Export files into segments of non-silent audio from `start_time` to `end_time`
  * `aud.split_by_silence(wav=WAV_PATH, theta=-35)`
  * `theta` is the silence threshold (default is -35dB)
3. Cutting based on chunks of time
  * Export files into `x` seconds clips
  * `aud.chunkify(wav=WAV_PATH, seconds=x)`


## Future Developments
* Support for strong temporal stamp files
  * In progress
* More robust file reading
* More audio editing features

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
