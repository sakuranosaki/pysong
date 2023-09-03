import math
import random
import pyaudio_common as common
from pyoscillator import Oscillator as osc


class PySynth:
    mix_sin = 0.3
    mix_square = 0.6
    mix_triangle = 0
    mix_noise = 0.1
    mix_saw = 0.0

    attack = 0.0  # sec
    decay = 0.2  # sec
    sustain = -6  # dB
    release = 0.1  # sec

    glide_head = 0.2  # sec
    glide_tail = 0.2  # sec

    detune = 0.0  # semitone]
    ring_mod_mix = 0
    ring_mod_freq_ratio = 5.5

    vib_min_duration = 0.7
    octave_shift = 0

    def mix_wave(self, theta):
        theta = math.fmod(theta, 2 * math.pi)
        result = 0.0
        result += math.sin(theta) * self.mix_sin
        result += osc.square(theta) * self.mix_square
        result += osc.saw(theta) * self.mix_saw
        result += osc.triangle(theta) * self.mix_triangle
        result += osc.noise() * self.mix_noise
        return result

    def create_notes(self, notes, duration):
        data = [0] * int(common.WAV_FREQ * (duration + self.release))
        for note in notes:
            freq = PySynth.freq_from_note(note, self.octave_shift)
            result = self._create_chromatic(freq, duration)
            result = self._apply_envelope(result, duration)
            if self.ring_mod_mix > 0:
                result = self._apply_am(result, freq)
            for i in range(0, len(data)):
                data[i] += result[i]

        return data

    def _create_chromatic(self, base_freq, duration):
        total_duration = duration + self.release

        gain = -16
        data = [0] * int(common.WAV_FREQ * total_duration)
        theta = 0
        vib_start = common.WAV_FREQ * max(total_duration / 2, self.vib_min_duration)

        for i in range(0, len(data)):
            if i < common.WAV_FREQ * self.glide_head:
                r = i / (common.WAV_FREQ * self.glide_head)
                freq = (1 - r) * base_freq / 2 + r * base_freq
            elif i > common.WAV_FREQ * (total_duration - self.glide_tail):
                r = (i - common.WAV_FREQ * (total_duration - self.glide_tail)) / (
                    self.glide_tail * common.WAV_FREQ
                )
                freq = (1 - r) * base_freq + r * (base_freq / 2)
            elif i > vib_start:
                freq = base_freq + math.sin(i / common.WAV_FREQ * math.pi * 2 * 7) * 5
            else:
                freq = base_freq

            freq = freq * math.pow(2, self.detune / 12)

            theta += 2 * math.pi * freq / common.WAV_FREQ
            theta = math.fmod(theta, math.pi * 2)
            data[i] = common.ratio_from_gain(gain) * self.mix_wave(theta)
        return data

    def _apply_envelope(self, data, duration):
        total_duration = duration + self.release
        decay_start = int(common.WAV_FREQ * self.attack)
        decay_end = int(common.WAV_FREQ * (self.attack + self.decay))
        release_start = int(common.WAV_FREQ * duration)
        decay_end = min(decay_end, release_start)

        for i in range(0, int(common.WAV_FREQ * total_duration)):
            if i < decay_start:
                r = i / decay_start
                data[i] *= common.ratio_from_gain(-60 * (1 - r))
            elif i < decay_end:
                r = (i - decay_start) / (decay_end - decay_start)
                data[i] *= common.ratio_from_gain(self.sustain * r)
            elif i < release_start:
                data[i] *= common.ratio_from_gain(self.sustain)
            else:
                r = (i - release_start) / (common.WAV_FREQ * self.release)
                data[i] *= common.ratio_from_gain(-60 * r + self.sustain)

        return data

    def _apply_am(self, data, freq):
        for i in range(len(data)):
            n = data[i] * math.sin(
                2 * math.pi * i * freq * self.ring_mod_freq_ratio / common.WAV_FREQ
            )
            data[i] = data[i] * (1 - self.ring_mod_mix) + n * self.ring_mod_mix
        return data

    def freq_from_note(note: str, octave_shift: int = 0):
        notes = {
            "C": 0,
            "D": 2,
            "E": 4,
            "F": 5,
            "G": 7,
            "A": 9,
            "B": 11,
            "C#": 1,
            "D#": 3,
            "F#": 6,
            "G#": 8,
            "A#": 10,
            "Db": 1,
            "Eb": 3,
            "Gb": 6,
            "Ab": 8,
            "Bb": 10,
        }

        (height, oct) = note.split()
        oct = int(oct)
        oct += octave_shift
        return 36.708 * math.pow(2, (notes[height] + oct * 12) / 12)
