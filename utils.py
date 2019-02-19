import os
import subprocess
import pickle
import glob
from music21 import converter, instrument, note, chord, stream


def get_notes():
    """
    从 music_midi 目录中的所有 MIDI 文件里提取 note（音符）和 chord（和弦）
    Note 样例： A, B, A#, B#, G#, E, ...
    Chord 样例: [B4 E5 G#5], [C5 E5], ...
    因为 Chord 就是多个 Note 的集合，所以把它们简单地统称为 “Note”
    """
    # 确保包含所有 MIDI 文件的 music_midi 文件夹在所有 Python 文件的同级目录下
    if not os.path.exists("music_midi"):
        raise Exception("包含所有 MIDI 文件的 music_midi 文件夹不在此目录下，请添加")

    notes = []

    # glob : 匹配所有符合条件的文件，并以 List 的形式返回
    for midi_file in glob.glob("music_midi/*.mid"):
        stream = converter.parse(midi_file)

        parts = instrument.partitionByInstrument(stream)

        if parts:  # 如果有乐器部分， 取第一个乐器部分
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = stream.flat.notes

        for element in notes_to_parse:
            # 如果是 Note 类型，那么取它的音调
            if isinstance(element, note.Note):
                # 格式例如： E6
                notes.append(str(element.pitch))
            # 如果是 Chord 类型，那么取它各个音调的序号
            elif isinstance(element, chord.Chord):
                # 转换后格式例如： 4.15.7
                notes.append('.'.join(str(n) for n in element.normalOrder))

    # 如果 data 目录不存在，创建此目录
    if not os.path.exists("data"):
        os.mkdir("data")
    # 将数据写入 data 目录下的 notes 文件
    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes


def create_music(prediction):
    """
    用神经网络'预测'的音乐数据来生成 MIDI 文件，再转成 MP3 文件
    """
    offset = 0   # 偏移
    output_notes = []

    # 生成 Note（音符）或 Chord（和弦）对象
    for data in prediction:
        # 是 Chord。格式例如： 4.15.7
        if ('.' in data) or data.isdigit():
            notes_in_chord = data.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()  # 乐器用钢琴 (piano)
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # 是 Note
        else:
            new_note = note.Note(data)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # 每次迭代都将偏移增加，这样才不会交叠覆盖
        offset += 0.5

    # 创建音乐流（Stream）
    midi_stream = stream.Stream(output_notes)

    # 写入 MIDI 文件
    midi_stream.write('midi', fp='output.mid')
