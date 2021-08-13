# Visual
Assist to Visually Impaired People

Installation
Requirements
Python 3 needs to be installed. Install Python 3 with Anaconda

Once Python 3 is installed, Clone this repository and then create a conda environment

conda create -n visual python=3.8
conda activate visual
conda install -c anaconda pyaudio
pip install -r requirements.txt


Donload yolv3 weights from https://pjreddie.com/darknet/yolo/

How to run the project
Go to the project directory and make sure conda environment is active. If not then you can activate by running below command

conda activate visual

Now start server by running

python main.py

