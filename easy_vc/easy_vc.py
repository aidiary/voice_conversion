#coding: utf-8
import pyaudio
import struct
import subprocess

# SPTKを使った簡単なボイスチェンジャー

CHANNELS = 1
RATE = 16000
CHUNK = 1024

def record(raw_file, record_seconds=5):
    """音声ファイルを録音する
    録音時間は固定。キーボードを押すとループ終わりができなかった・・・"""
    fp = open(raw_file, "wb")
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        fp.write(struct.pack('s' * CHUNK * 2, *data))
    fp.close()
    stream.stop_stream()
    stream.close()
    p.terminate()

def extract_pitch(raw_file, pitch_file):
    """ピッチパラメータの抽出"""
    cmd = "x2x +sf %s | pitch -a 1 -s 16 -p 80 > %s" % (raw_file, pitch_file)
    subprocess.call(cmd, shell=True)

def extract_mcep(raw_file, mcep_file):
    """メルケプストラムパラメータの抽出"""
    cmd = "x2x +sf %s | frame -p 80 | window | mcep -m 25 -a 0.42 > %s" % (raw_file, mcep_file)
    subprocess.call(cmd, shell=True)

def modify_pitch(m, pitch_file, mcep_file, raw_file):
    """ピッチを変形して再合成
    mが1より大きい => 低い声
    mが1より小さい => 高い声"""
    cmd = "sopr -m %f %s | excite -p 80 | mlsadf -m 25 -a 0.42 -p 80 %s | clip -y -32000 32000 | x2x +fs > %s" % (m, pitch_file, mcep_file, raw_file)
    subprocess.call(cmd, shell=True)

def modify_speed(frame_shift, pitch_file, mcep_file, raw_file):
    """話速を変形して再合成
    frame_shiftが小さい => 早口
    frame_shiftが大きい => ゆっくり"""
    cmd = "excite -p %f %s | mlsadf -m 25 -a 0.42 -p %f %s | clip -y -32000 32000 | x2x +fs > %s" % (frame_shift, pitch_file, frame_shift, mcep_file, raw_file)
    subprocess.call(cmd, shell=True)

def hoarse_voice(pitch_file, mcep_file, raw_file):
    """ささやき声"""
    modify_pitch(0, pitch_file, mcep_file, raw_file)

def robot_voice(frame_period, record_seconds, mcep_file, raw_file):
    """ロボット声
    frame_periodが小さい => 低い
    frame_periodが大きい => 高い"""
    sequence_length = record_seconds * RATE * frame_period
    cmd = "train -p %d -l %d | mlsadf -m 25 -a 0.42 -p 80 %s | clip -y -32000 32000 | x2x +fs > %s" % (frame_period, sequence_length, mcep_file, raw_file)
    subprocess.call(cmd, shell=True)

def child_voice(pitch_file, mcep_file, raw_file):
    """子供声"""
    cmd = "sopr -m 0.4 %s | excite -p 80 | mlsadf -m 25 -a 0.1 -p 80 %s | clip -y -32000 32000 | x2x +fs > %s" % (pitch_file, mcep_file, raw_file)
    subprocess.call(cmd, shell=True)

def deep_voice(pitch_file, mcep_file, raw_file):
    """深い声"""
    cmd = "sopr -m 2.0 %s | excite -p 80 | mlsadf -m 25 -a 0.6 -p 80 %s | clip -y -32000 32000 | x2x +fs > %s" % (pitch_file, mcep_file, raw_file)
    subprocess.call(cmd, shell=True)

def raw2wav(raw_file, wav_file):
    cmd = "sox -e signed-integer -c %d -b 16 -r %d %s %s" % (CHANNELS, RATE, raw_file, wav_file)
    subprocess.call(cmd, shell=True)

def play(raw_file):
    """rawファイルを再生"""
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2), channels=CHANNELS, rate=RATE, output=True)
    f = open(raw_file, "rb")
    data = f.read(CHUNK)
    while data != '':
        stream.write(data)
        data = f.read(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    # 録音時間（固定）
    record_seconds = 10

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    pitch_file = "temp.pitch"
    mcep_file = "temp.mcep"
    raw_file = "temp.raw"
    output_file = "output.raw"

    # オリジナルの音声を録音してrawファイルとして書き出し
    print "*** Now recording ... (%d sec)" % record_seconds
    record(raw_file, record_seconds)

    # パラメータ抽出
    print "*** extract pitch ..."
    extract_pitch(raw_file, pitch_file)

    print "*** extract mel cepstrum"
    extract_mcep(raw_file, mcep_file)

    # パラメータ変形いろいろ
    print "*** modify parameters ..."

    # どれか一つしか有効にできない
#    modify_pitch(0.3, pitch_file, mcep_file, output_file)
#    modify_speed(300, pitch_file, mcep_file, output_file)
#    hoarse_voice(pitch_file, mcep_file, output_file)
#    robot_voice(100, record_seconds, mcep_file, output_file)
#    child_voice(pitch_file, mcep_file, output_file)
    deep_voice(pitch_file, mcep_file, output_file)

    # 変換した音声を再生
    print "*** play!"
    play("output.raw")
