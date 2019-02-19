**********************工程环境**********************
OS：Windows 10 1809
CPU：Intel i5-6300HQ
GPU：NVIDIA GTX960M
Python：3.6.7
Tensorflow-gpu：1.8
cuda：9.0
cuDNN：7.0
**********************模块库**********************
os
subprocess
pickle
glob
music21
numpy
tensorflow
**********************代码说明**********************
本工程下各文件的功能如下：
music_midi：训练所用的 MIDI 文件
generate.py：用训练好的神经网络模型参数来作曲
network.py：RNN-LSTM 循环神经网络
train.py：训练神经网络，将参数（Weight）存入 HDF5 文件
utils.py：包含一些处理函数
output.mid：神经网络输出音乐样例
output.mp3：神经网络输出音乐样例MP3格式

