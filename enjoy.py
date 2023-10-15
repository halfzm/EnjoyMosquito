import time
import wave
import random

import pyaudio


def play(fp):
    # 打开音频文件
    wf = wave.open(fp, 'rb')

    # 初始化PyAudio对象
    p = pyaudio.PyAudio()

    # 设置参数
    rate = wf.getframerate()
    channels = wf.getnchannels()
    sample_format = p.get_format_from_width(wf.getsampwidth())
    chunk = 1024

    # 打开流
    stream = p.open(rate=rate,
                    channels=channels,
                    format=sample_format,
                    output=True,
                    frames_per_buffer=chunk)

    print("开始播放...")
    data = wf.readframes(chunk)
    try:
        while data:
            # 读取音频数据并播放
            # 以防播放过程中拔掉耳机
            try:
                stream.write(data)
                data = wf.readframes(chunk)
            except:
                break
        print("播放结束...")
    except:
        print("播放结束...")
    finally:
        # 关闭流和PyAudio对象
        # 以防播放过程中拔掉耳机
        try:
            stream.stop_stream()
            stream.close()
        except:
            pass
        p.terminate()


def is_headphones_plugged():
    p = pyaudio.PyAudio()
    device_info = p.get_default_output_device_info()
    # print(device_info)
    if not device_info['name'].startswith('扬声器') and device_info['name'].startswith('鑰虫満'):
        print("耳机已插入...")
        p.terminate()
        return True
    print('未检测到耳机...')
    p.terminate()
    return False



if __name__ == '__main__':
    while True:
        if is_headphones_plugged():
            play('happy.wav')
        print('等待...')
        # 随机10到100秒检测一次
        sleep_time = random.randint(10, 100)
        time.sleep(sleep_time)
