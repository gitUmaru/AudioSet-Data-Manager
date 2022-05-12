import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audioset-manager", # Replace with your own username
    version="0.0.8",
    author="Muhammad Umar Ali",
    author_email="umaruali@student.ubc.ca",
    description="A simple python package for managing the audio data from Google Research's ontology of 632 audio event classes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitUmaru/AudioSet-Data-Manager",
    packages=setuptools.find_packages(),
    package_data={'audiosetmanager': ['AudioSet Data/*.txt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       "pydub",
       "youtube_dl",
       "pandas"
   ]
)
\
