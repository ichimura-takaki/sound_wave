import math
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

class HzScond:
    def __init__(self, frequency,duration):
        
        # 基本設定
        self.frequency = frequency  # Hz（周波数）
        self.duration = duration  # 秒
        self.sampling_rate = 44100  # 標準的なサンプリングレート
        self.t = None
        self.signal = None

    def volume(self,volume_level):
        # 音量を設定（0-100の範囲）
        scaled_volume = volume_level / 100
        if self.signal is not None:
            self.signal *= scaled_volume
        return self
    
    def play(self):
        # グラフ描画
        plt.plot(self.t, self.signal)
        plt.title(str(self.frequency)+"Hz wave")
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.xlim(0, 0.01)  # 表示範囲を0〜0.01秒に限定
        sd.play(self.signal, samplerate=self.sampling_rate)  # 音を再生
        plt.show()  # グラフを表示
        sd.wait()  # 再生が終わるまで待機

    def play_with_volume(self,volume_level):
        # 音量を設定して再生
        self.volume(volume_level)
        self.play()

    def adsr(self,attack, decay, sustain, release):
        # ADSRエンベロープを適用
        total_samples = int(self.sampling_rate * self.duration)
        envelope = np.zeros(total_samples)

        # Attack phase
        attack_samples = int(self.sampling_rate * attack)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        # Decay phase
        decay_samples = int(self.sampling_rate * decay)
        sustain_level = sustain
        envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples)

        # Sustain phase
        sustain_samples = total_samples - (attack_samples + decay_samples + int(self.sampling_rate * release))
        envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain_level

        # Release phase
        release_start = attack_samples + decay_samples + sustain_samples
        envelope[release_start:] = np.linspace(sustain_level, 0, total_samples - release_start)

        self.signal *= envelope
        return self


    def sine_wave(self):
        # 時間軸を生成
        self.t = np.linspace(0, self.duration, int(self.sampling_rate * self.duration), endpoint=False)
        # 正弦波を生成（振幅は1.0）
        self.signal = np.sin(2 * math.pi * self.frequency * self.t)
        return self
    
    def square_wave(self):
        # 時間軸を生成
        self.t = np.linspace(0, self.duration, int(self.sampling_rate * self.duration), endpoint=False)
        # 矩形波を生成（正弦波の符号を使って +1 or -1 の値に）
        self.signal = np.sign(np.sin(2 * math.pi * self.frequency * self.t))
        return self
    
    def Yis1(self):
        # 時間軸を生成
        self.t = np.linspace(0, self.duration, int(self.sampling_rate * self.duration), endpoint=False)
        # 振幅を1に設定
        AMPLITUBE = 1.0
        self.signal = np.ones(int(self.sampling_rate * self.duration)) * AMPLITUBE
        return self

    
if __name__ == "__main__":
    HzScond(440,1).sine_wave().play_with_volume(1)
    #HzScond(440,1).square_wave().play_with_volume(1)
    #HzScond(440,1).Yis1().play_with_volume(1)
    #HzScond(440,1).sine_wave().adsr(0,0,0,0).play_with_volume(1)
    pass