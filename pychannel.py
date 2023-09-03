import pyaudio_common as common
import soundfile as sf
import numpy as np
import os


class Channel:
    bpm = 172

    _length = 0
    _path = ""
    _use_cache = True

    def __init__(self, bpm, bar, path, channel=1, use_cache=True):
        self.bpm = bpm
        length = int(60 / self.bpm * bar * 4) * common.WAV_FREQ
        self._length = length
        self.channels = []
        for i in range(channel):
            self.channels.append([0] * length)
        self._path = path
        self._use_cache = use_cache

    def try_load(self):
        if self._use_cache and self.read():
            return True
        return False

    def add(self, samples, bar, beat, tick, gain, channel=0):
        t = (bar * 4 + beat + tick / 480) / self.bpm * 60
        position = int(t * common.WAV_FREQ)
        self._add(samples, position, gain, channel)

    def _add(self, samples, position, gain, channel=0):
        r = common.ratio_from_gain(gain)
        for i in range(0, len(samples)):
            self.channels[channel][position + i] += samples[i] * r

    def write(self):
        sf.write(
            self._path, np.array(self.channels).T, common.WAV_FREQ, subtype="PCM_16"
        )

    def read(self):
        if os.path.exists(self._path):
            self.channels, _ = sf.read(self._path)
            self.channels = [self.channels]
            self._length = len(self.channels)
            return True
        return False

    def calc_duration(self, bar, beat, tick):
        return (bar * 4 + beat + tick / 480) / self.bpm * 60

    def normalize(self):
        max = 0
        for ch in range(0, len(self.channels)):
            for i in range(0, len(self.channels[ch])):
                if abs(self.channels[ch][i]) > max:
                    max = abs(self.channels[ch][i])

        print("max:" + str(max))
        ratio = 1 / max
        for ch in range(0, len(self.channels)):
            for i in range(0, len(self.channels[ch])):
                self.channels[ch][i] *= ratio

    def delay(self, delay_time, gain):
        ratio = common.ratio_from_gain(gain)
        delay_samples = int(delay_time * common.WAV_FREQ)
        for ch in range(len(self.channels)):
            for i in range(len(self.channels[ch]) - delay_samples):
                self.channels[ch][i + delay_samples] += self.channels[ch][i] * ratio

    def soft_limit(self, gain):
        for ch in range(len(self.channels)):
            self.channels[ch] = common.soft_limit(self.channels[ch], gain)

    def fade_out(self, start_time):
        start_sample = int(start_time * common.WAV_FREQ)
        for ch in range(len(self.channels)):
            for i in range(start_sample, len(self.channels[ch])):
                r = (i - start_sample) / (len(self.channels[ch]) - start_sample)
                ratio = common.ratio_from_gain(r * -60)
                self.channels[ch][i] *= ratio

    def equalizer(self, freq, Q, gain):
        for ch in range(len(self.channels)):
            self.channels[ch] = common.biquad_equalizer(
                self.channels[ch], freq, Q, gain
            )

    def lowpass(self, freq, Q):
        for ch in range(len(self.channels)):
            self.channels[ch] = common.biquad_lowpass(self.channels[ch], freq, Q)
