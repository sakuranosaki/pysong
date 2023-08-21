import math
import random

import pyaudio_common as common

class PyDrum:
    
    _bd = []
    _hh = []
    _sd = []
    _cy = []
    _pu = []
    _bpm = 120
    _patterns = {}
    _data = []
    
    def __init__(self, bpm):
        self._bd = PyDrum.create_bass_drum()
        self._hh = PyDrum.create_hihat()
        self._sd = PyDrum.create_snare_drum()
        self._cy = PyDrum.create_cymbal()
        self._pu = PyDrum.create_popup()
        self._bpm = bpm
    
    def set_pattern(self, id, pattern):
        self._patterns[id] = pattern    
    
    def calc_patterns(self, pattern_ids):
        bar_length = int(4 * common.WAV_FREQ * 60 / self._bpm)
        self._data = [0] * (len(pattern_ids)+1) * bar_length
        
        for bar_index, pattern_id in enumerate(pattern_ids):
            pattern = self._patterns[pattern_id]
            for (key, value) in pattern.items():
                for index, note in enumerate(value):
                    if note != 0:
                        pos = bar_index * bar_length + index * bar_length // 16 # 16th
                        if key == 'bd':
                            self.mix(pos, self._bd, -3)
                        elif key == 'hh':
                            self.mix(pos, self._hh, -7)
                        elif key == 'sd':
                            self.mix(pos, self._sd, -1)
                        elif key == 'cy':
                            self.mix(pos, self._cy, -6)
                        elif key == 'pu':
                            self.mix(pos, self._pu, -22)
   
        common.soft_limit(self._data, -6)
        return self._data
    
    def mix(self, position, data, gain):
        ratio = common.ratio_from_gain(gain)
        for i in range(0, len(data)):
            self._data[position + i] += data[i] * ratio
    
    def create_bass_drum(length = common.WAV_FREQ // 5):
        data = [0] * length
        ratio = [1.00, 1.31, 1.60, 1.88]

        sheta = [0] * len(ratio)
        freq = 0
        for i in range(length):

            # ピッチダウン            
            if i < 2000:
                pitch_ratio = i / 2000
                freq = (55.000*3) * (1-pitch_ratio) + 55.000 * pitch_ratio
            else:
                freq = 60
            
            # 今回追加する角度

            # サイン波の合成
            for ratio_index in range(len(ratio)):        
                sheta[ratio_index] += math.pi * 2 * freq * ratio[ratio_index] / common.WAV_FREQ
                sheta[ratio_index] %= math.pi * 2
                level = 1 / ((ratio_index+1) ** 3)
                data[i] += math.sin(sheta[ratio_index]) * level * 0.5            
            
            # ビーターの計算
            beater = 0
            if(i < 441):
                data[i] += random.uniform(-0.05, 0.05)
            
            # 減衰の計算
            p = math.pow(i / length, 5)
            data[i] *= common.ratio_from_gain(p * -60)

        return data

    def create_hihat():
        data = []
        length = common.WAV_FREQ // 7
        
        for i in range(length):
            r = i / length
            noise = random.uniform(-0.5, 0.5)
            data.append(noise * common.ratio_from_gain(r * -60))

        return data

    def create_snare_drum():
        data = []
        length = common.WAV_FREQ // 6
        pitch_from = 250
        pitch_to = 280
        delta_from = math.pi * 2 * pitch_from / common.WAV_FREQ
        delta_to   = math.pi * 2 * pitch_to / common.WAV_FREQ
        shita = 0
        for i in range(length):
            r = i / length
            p = math.pow(r, 2)
            shita += (1-r) * delta_from + r * delta_to
            beater = random.uniform(-0.3, 0.3)
            data.append((math.sin(shita) * 0.3 + beater) * common.ratio_from_gain(p * -60))

        return data

    def create_popup():
        data = []
        length = common.WAV_FREQ // 6
        pitch_from = 300
        pitch_to = 4000
        delta_from = math.pi * 2 * pitch_from / common.WAV_FREQ
        delta_to   = math.pi * 2 * pitch_to / common.WAV_FREQ
        shita = 0
        for i in range(length):
            r = i / length
            p = math.pow(r, 2)
            shita += (1-r) * delta_from + r * delta_to
            data.append(PyDrum._square(shita))
        return data

    def _square(t):
        t = t % (math.pi * 2)
        if t < math.pi:
            return 1
        else:
            return -1
        
    def create_cymbal():
        duration = 1
        data = []
        for i in range(0, int(common.WAV_FREQ * duration)):
            r = i / (common.WAV_FREQ * duration)
            data.append(random.uniform(-0.5, 0.5) * common.ratio_from_gain(r * -60))
        
        data = common.biquad_equalizer(data, 4000, 20, 8)
        data = common.biquad_equalizer(data, 8000, 20, 4)
        return data
