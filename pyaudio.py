from pychannel import Channel
import pysynth
import pydrum

import numpy as np
from scipy.special import jn_zeros
import soundfile as sf
import pyaudio_common as common

SONG_BPM = 174

def main():
    make_song()

def make_song():
    total_bar = 27
    channel_dr = Channel(SONG_BPM, total_bar, "./ch_drum.wav")
    if not channel_dr.try_load():
        calc_drum_channel(channel_dr)
        channel_dr.write()

    channel_chordL = Channel(SONG_BPM, total_bar, "./ch_chordL.wav")
    if not channel_chordL.try_load():
        calc_chord_channel(channel_chordL, True)
        channel_chordL.write()

    channel_chordR = Channel(SONG_BPM, total_bar, "./ch_chordR.wav")
    if not channel_chordR.try_load():
        calc_chord_channel(channel_chordR, False)
        channel_chordR.write()

    channel_bass = Channel(SONG_BPM, total_bar, "./ch_bass.wav")
    if not channel_bass.try_load():
        calc_bass_channel(channel_bass)
        channel_bass.write()

    channel_melody = Channel(SONG_BPM, total_bar, "./ch_melody.wav")
    if not channel_melody.try_load():
        calc_melody_channel(channel_melody, False)
        channel_melody.write()

    channel_melody_rm = Channel(SONG_BPM, total_bar, "./ch_melody_bell.wav")
    if not channel_melody_rm.try_load():
        calc_melody_channel(channel_melody_rm, True)
        channel_melody_rm.write()

    channel_pico = Channel(SONG_BPM, total_bar, "./ch_pico.wav")
    if not channel_pico.try_load():
        calc_pico_channel(channel_pico)
        channel_pico.write()
    
    channel_master = Channel(SONG_BPM, total_bar, "./song.wav", 2, False)
    for ch in range(2):
        channel_master.add(channel_dr.data[0], 0, 0, 0, -2, ch)
        channel_master.add(channel_bass.data[0], 0, 0, 0, 1, ch)
        channel_master.add(channel_melody.data[0], 0, 0, 0, 0, ch)
        channel_master.add(channel_melody_rm.data[0], 0, 0, 0, -2, ch)
        channel_master.add(channel_pico.data[0], 0, 0, 0, -2, ch)

    channel_master.add(channel_chordL.data[0], 0, 0, 0, -8, 0)
    channel_master.add(channel_chordR.data[0], 0, 0, 0, -8, 1)
    
    channel_master.equalizer(2000, 0.3, 3)
    channel_master.lowpass(20000, 0.3)
    channel_master.soft_limit(-8)
    
    channel_master.normalize()
    channel_master.fade_out(len(channel_master.data[0]) / 44100 - 10)
    channel_master.write()

def calc_pico_channel(channel : Channel):
    pico_synth = pysynth.PySynth()
    pico_synth.mix_noise = 0
    pico_synth.mix_square = 0.7
    pico_synth.mix_triangle = 0
    pico_synth.mix_saw = 0.0
    pico_synth.mix_sin = 0.3
    pico_synth.attack = 0
    pico_synth.decay = 0
    pico_synth.sustain = 0
    pico_synth.release = 0.05
    pico_synth.glide_head = 0
    pico_synth.glide_tail = 0
    pico_synth.vib_min_duration = 1
    
    pico = [
        "R  |480", "R  |480",
        "A 1| 60", "C 2| 60", "D 2| 60", "G 2| 60",
        "A 2| 60", "C 3| 60", "D 3| 60", "G 3| 60",
        "A 3| 60", "C 4| 60", "D 4| 60", "G 4| 60",
        "A 4| 60", "C 5| 60", "D 5| 60", "G 5| 60",
        "R  |1920",
        "R  |1920",
        "R  |1920",
        "A 1| 60", "C 2| 60", "D 2| 60", "G 2| 60",
        "A 2| 60", "C 3| 60", "D 3| 60", "G 3| 60",
        "A 2| 60", "C 3| 60", "D 3| 60", "G 3| 60",
        "A 3| 60", "C 4| 60", "D 4| 60", "G 4| 60",
        "A 3| 60", "C 4| 60", "D 4| 60", "G 4| 60",
        "A 4| 60", "C 5| 60", "D 5| 60", "G 5| 60",
        "R  |480",
        "G 5| 60", "E 5| 60", "D 5| 60", "C 5| 60",
        "G 4| 60", "E 4| 60", "D 4| 60", "C 4| 60",
        "G 4| 60", "E 4| 60", "D 4| 60", "C 4| 60",
        "G 3| 60", "E 3| 60", "D 3| 60", "C 3| 60",
        "G 3| 60", "E 3| 60", "D 3| 60", "C 3| 60",
        "G 2| 60", "E 2| 60", "D 2| 60", "C 2| 60",
        "R  |480",
        "G 5| 60", "F 5| 60", "D 5| 60", "C 5| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "C 4| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "C 4| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "C 3| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "C 3| 60",
        "G 2| 60", "F 2| 60", "D 2| 60", "C 2| 60",
        "R  |480",
        "G 5| 60", "F 5| 60", "D 5| 60", "B 4| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "B 3| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "B 3| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "B 2| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "B 2| 60",
        "G 2| 60", "F 2| 60", "D 2| 60", "B 1| 60",
        "R  |480",
        "A 1| 60", "C 2| 60", "D 2| 60", "G 2| 60",
        "A 2| 60", "C 3| 60", "D 3| 60", "G 3| 60",
        "A 2| 60", "C 3| 60", "D 3| 60", "G 3| 60",
        "A 3| 60", "C 4| 60", "D 4| 60", "G 4| 60",
        "A 3| 60", "C 4| 60", "D 4| 60", "G 4| 60",
        "A 4| 60", "C 5| 60", "D 5| 60", "G 5| 60",
        "R  |480",
        "G 5| 60", "E 5| 60", "D 5| 60", "C 5| 60",
        "G 4| 60", "E 4| 60", "D 4| 60", "C 4| 60",
        "G 4| 60", "E 4| 60", "D 4| 60", "C 4| 60",
        "G 3| 60", "E 3| 60", "D 3| 60", "C 3| 60",
        "G 3| 60", "E 3| 60", "D 3| 60", "C 3| 60",
        "G 2| 60", "E 2| 60", "D 2| 60", "C 2| 60",
        "R  |480",
        "G 5| 60", "F 5| 60", "D 5| 60", "C 5| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "C 4| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "C 4| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "C 3| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "C 3| 60",
        "G 2| 60", "F 2| 60", "D 2| 60", "C 2| 60",
        "R  |480",
        "G 5| 60", "F 5| 60", "D 5| 60", "B 4| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "B 3| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "B 3| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "B 2| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "B 2| 60",
        "G 2| 60", "F 2| 60", "D 2| 60", "B 1| 60",
        "R  |480",
        "A 1| 60", "C 2| 60", "D 2| 60", "G 2| 60",
        "A 2| 60", "C 3| 60", "D 3| 60", "G 3| 60",
        "A 2| 60", "C 3| 60", "D 3| 60", "G 3| 60",
        "A 3| 60", "C 4| 60", "D 4| 60", "G 4| 60",
        "A 3| 60", "C 4| 60", "D 4| 60", "G 4| 60",
        "A 4| 60", "C 5| 60", "D 5| 60", "G 5| 60",
        "R  |480",
        "G 5| 60", "E 5| 60", "D 5| 60", "C 5| 60",
        "G 4| 60", "E 4| 60", "D 4| 60", "C 4| 60",
        "G 4| 60", "E 4| 60", "D 4| 60", "C 4| 60",
        "G 3| 60", "E 3| 60", "D 3| 60", "C 3| 60",
        "G 3| 60", "E 3| 60", "D 3| 60", "C 3| 60",
        "G 2| 60", "E 2| 60", "D 2| 60", "C 2| 60",
        "R  |480",
        "G 5| 60", "F 5| 60", "D 5| 60", "C 5| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "C 4| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "C 4| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "C 3| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "C 3| 60",
        "G 2| 60", "F 2| 60", "D 2| 60", "C 2| 60",
        "R  |480",
        "G 5| 60", "F 5| 60", "D 5| 60", "B 4| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "B 3| 60",
        "G 4| 60", "F 4| 60", "D 4| 60", "B 3| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "B 2| 60",
        "G 3| 60", "F 3| 60", "D 3| 60", "B 2| 60",
        "G 2| 60", "F 2| 60", "D 2| 60", "B 1| 60",
        "R  |480",
        "A 1| 60", "C 2| 60", "D 2| 60", "G 2| 60",
        "A 2| 60", "C 3| 60", "D 3| 60", "G 3| 60",
        "A 2| 60", "C 3| 60", "D 3| 60", "G 3| 60",
        "A 3| 60", "C 4| 60", "D 4| 60", "G 4| 60",
        "A 3| 60", "C 4| 60", "D 4| 60", "G 4| 60",
        "A 4| 60", "C 5| 60", "D 5| 60", "G 5| 60",
    ] 
    
    current_tick = 0
    pico_data = {}
    for m in pico:
        note, duration = m.split('|')
        note_duration = int(duration) * 0.75
        if not note.startswith('R'):
            if not m in pico_data:
                data = pico_synth.create_notes([note], channel.calc_duration(0, 0, note_duration))
                pico_data[m] = data
            channel.add(pico_data[m], 0, 0, current_tick, -12)
        current_tick += int(duration)
    
    channel.delay(0.3, -12)
    channel.delay(0.5, -16)

def calc_melody_channel(channel : Channel, enable_ring_mod : bool):
    melody_synth = pysynth.PySynth()
    melody_synth.mix_noise = 0
    melody_synth.mix_square = 0.5
    melody_synth.mix_triangle = 0
    melody_synth.mix_saw = 0.4
    melody_synth.mix_sin = 0.1
    melody_synth.attack = 0
    melody_synth.decay = 0.1
    melody_synth.sustain = -6
    melody_synth.release = 0
    melody_synth.glide_head = 0
    melody_synth.glide_tail = 0
    melody_synth.vib_min_duration = 0.2

    if enable_ring_mod:
        melody_synth.ring_mod_mix = 0.5
        melody_synth.attack = 0
        melody_synth.decay = 2
        melody_synth.sustain = -12
        melody_synth.release = 1
        melody_synth.octave_shift = 1
        melody_synth.detune = 0.2
        
    
    melody = [
        "R  |960", "R  |240", "E 4|240", "E 4|240", "F 4|240",
        "G 4|480", "G 4|240", "G 4|480", "G 4|240", "A 4|240", "G 4|480",
        "C 4|240", "C 4|240", "C 4|480", "R  |240", "E 4|240", "F 4|240",
        "G 4|480", "G 4|240", "G 4|480", "G 4|240", "C 5|240", "B 4|480",
        "G 4|720", "R  |240", "E 4|240", "E 4|240", "F 4|240",
        "G 4|480", "G 4|240", "G 4|480", "A 4|480", "G 4|480", "F 4|240", "E 4|480", "R  |480",
        "E 4|240", "F 4|240", "E 4|240", "D 4|480", "C 4|480", "D 4|240", "C 4|240", "E 4|1200", "R  |240",
        "E 4|240", "E 4|240", "F 4|240",
        "G 4|480", "G 4|240", "G 4|480", "G 4|240", "A 4|240", "G 4|480",
        "C 4|240", "C 4|240", "C 4|480", "R  |240", "E 4|240", "F 4|240",
        "G 4|480", "G 4|240", "G 4|480", "G 4|240", "C 5|240", "B 4|480",
        "G 4|720", "R  |240", "E 4|240", "E 4|240", "F 4|240",
        "G 4|480", "G 4|240", "G 4|480", "A 4|480", "G 4|480", "C 5|240", "B 4|240", "C 5|480", "R  |240",
        "A 4|240", "G 4|480", "F 4|480", "E 4|480", "D 4|240", "B 3|240", "C 4|1920",
    ]
    
    current_tick = 0
    melody_data = {}
    for m in melody:
        note, duration = m.split('|')
        if int(duration) == 240:
            note_duration = int(duration) * 0.5
        else:
            note_duration = int(duration) * 0.9
            
        if not note.startswith('R'):
            if not m in melody_data:
                data = melody_synth.create_notes([note], channel.calc_duration(0, 0, note_duration))
                melody_data[m] = data
            channel.add(melody_data[m], 0, 0, current_tick, -6)
        current_tick += int(duration)

    if not enable_ring_mod:
        channel.delay(0.4, -10)

def calc_bass_channel(channel : Channel):
    base_synth = pysynth.PySynth()
    base_synth.mix_noise = 0
    base_synth.mix_square = 0
    base_synth.mix_triangle = 0
    base_synth.mix_saw = 0.4
    base_synth.mix_sin = 0.6

    base_synth.glide_head = 0.1
    base_synth.glide_tail = 0.1

    baseC1 = base_synth.create_notes(["C 1"], channel.calc_duration(0, 1, 360))
    baseF1 = base_synth.create_notes(["F 1"], channel.calc_duration(0, 3, 240))
    baseG1 = base_synth.create_notes(["G 1"], channel.calc_duration(0, 1, 360))
    baseA0 = base_synth.create_notes(["A 0"], channel.calc_duration(0, 3, 240))

    base_synth.glide_head = 0.0
    base_synth.glide_tail = 0.0

    baseC1_sh = base_synth.create_notes(["C 1"], channel.calc_duration(0, 0, 120))
    baseC2_sh = base_synth.create_notes(["C 2"], channel.calc_duration(0, 0, 120))
    baseD1_sh = base_synth.create_notes(["D 1"], channel.calc_duration(0, 0, 120))
    baseE1_sh = base_synth.create_notes(["E 1"], channel.calc_duration(0, 0, 120))
    baseF1_sh = base_synth.create_notes(["F# 1"], channel.calc_duration(0, 0, 120))
    baseF2_sh = base_synth.create_notes(["F 2"], channel.calc_duration(0, 0, 120))
    baseA1_sh = base_synth.create_notes(["A 1"], channel.calc_duration(0, 0, 120))
    baseAb1_sh = base_synth.create_notes(["Ab 1"], channel.calc_duration(0, 0, 120))
    baseB0_sh = base_synth.create_notes(["B 0"], channel.calc_duration(0, 0, 120))

    base_gain = -6
    for i in range(6):
        bar = 1 + i * 4
        channel.add(baseC1,     bar + 0, 0, 0, base_gain)
        channel.add(baseC1_sh,  bar + 0, 2, 0, base_gain)
        channel.add(baseD1_sh,  bar + 0, 2, 240, base_gain)
        channel.add(baseE1_sh,  bar + 0, 3, 0, base_gain)
        channel.add(baseF1,     bar + 0, 3, 240, base_gain)
        channel.add(baseF2_sh,  bar + 1, 3, 0, base_gain)
        channel.add(baseC2_sh,  bar + 1, 3, 120, base_gain)
        channel.add(baseA1_sh,  bar + 1, 3, 240, base_gain)
        channel.add(baseAb1_sh, bar + 1, 3, 360, base_gain)
        channel.add(baseG1,     bar + 2, 0, 0, base_gain)
        channel.add(baseF1_sh,  bar + 2, 2, 0, base_gain)
        channel.add(baseD1_sh,  bar + 2, 2, 240, base_gain)
        channel.add(baseB0_sh,  bar + 2, 3, 0, base_gain)
        channel.add(baseA0,     bar + 2, 3, 240, base_gain)
    return channel

def calc_chord_channel(channel : Channel, isLeft = True):
    chord_synth = pysynth.PySynth()
    chord_synth.attack = 0.04
    chord_synth.release = 0
    chord_synth.mix_noise = 0.1
    chord_synth.mix_square = 0.5
    chord_synth.mix_triangle = 0.0
    chord_synth.mix_sin = 0.1
    chord_synth.mix_saw = 0.3
    
    if not isLeft:
        chord_synth.detune = 0.03
    
    chord_synth.glide_head = 0.1
    chord_synth.glide_tail = 0.15
    
    chord1 = chord_synth.create_notes(["C 1", "G 2", "D 3", "E 3", "G 3"], channel.calc_duration(0, 2, 0))
    chord2 = chord_synth.create_notes(["F 1", "C 3", "D 3", "F 3", "G 3"], channel.calc_duration(0, 3, 120))
    chord3 = chord_synth.create_notes(["G 1", "B 2", "D 3", "E 3", "G 3"], channel.calc_duration(0, 2, 0))
    chord4 = chord_synth.create_notes(["A 1", "D 3", "E 3", "G 3"], channel.calc_duration(1, 0, 0))
    chord4B = chord_synth.create_notes(["B 3"], channel.calc_duration(0, 1, 0))
    chord4C = chord_synth.create_notes(["C 4"], channel.calc_duration(0, 3, 0))

    chord_gain = 0
    for i in range(6):
        bar = 1 + i * 4
        channel.add(chord1, bar + 0, 0, 0, chord_gain)
        channel.add(chord2, bar + 0, 3, 240, chord_gain)
        channel.add(chord3, bar + 2, 0, 0, chord_gain)
        channel.add(chord4, bar + 2, 3, 240, chord_gain)
        channel.add(chord4B, bar + 2, 3, 240, chord_gain)
        channel.add(chord4C, bar + 3, 0, 240, chord_gain)

    channel.soft_limit(-6)

def calc_drum_channel(channel : Channel):
    drum = pydrum.PyDrum(SONG_BPM)
    drum.set_pattern(0, {
        "cy" : [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,1,0],
        "hh" : [0,0,1,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
        "sd" : [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
        "bd" : [1,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,1,0],
    })
    drum.set_pattern(1, {
        "cy" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
        "hh" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
        "sd" : [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
        "bd" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
    })
    drum.set_pattern(2, {
        "cy" : [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
        "hh" : [0,0,1,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
        "sd" : [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
        "bd" : [1,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,1,0],
    })
    drum.set_pattern(3, {
        "pu" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0],
        "cy" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
        "hh" : [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],
        "sd" : [0,0,1,1, 1,0,0,0, 1,0,0,0, 1,0,0,0],
        "bd" : [0,0,0,0, 0,0,1,0, 0,0,1,0, 0,0,1,0],
    })
    
    drum.set_pattern(4, {
        "cy" : [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,1,0],
        "hh" : [1,0,1,0, 1,1,1,0, 1,0,1,0, 1,0,1,1],
        "sd" : [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
        "bd" : [1,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,1,0],
    })
    drum.set_pattern(5, {
        "cy" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
        "hh" : [1,0,1,0, 1,1,1,0, 1,0,1,0, 1,0,1,1],
        "sd" : [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
        "bd" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
    })
    drum.set_pattern(6, {
        "cy" : [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
        "hh" : [1,0,1,0, 1,1,1,0, 1,0,1,0, 1,0,1,1],
        "sd" : [0,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
        "bd" : [1,0,0,0, 0,0,0,0, 0,0,1,0, 0,0,1,0],
    })
    drum.set_pattern(7, {
        "pu" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0],
        "cy" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
        "hh" : [1,0,1,0, 1,1,1,0, 1,0,1,0, 1,0,1,1],
        "sd" : [0,0,1,1, 1,0,0,0, 1,0,0,0, 1,0,0,0],
        "bd" : [0,0,0,0, 0,0,1,0, 0,0,1,0, 0,0,1,0],
    })

    drum.set_pattern(8, {
        "pu" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,0,0,0],
        "cy" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
        "hh" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
        "sd" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,1,1,1],
        "bd" : [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
    })
    
    result = drum.calc_patterns([8,0,1,2,3,0,1,2,3,4,5,6,7,4,5,6,7,0,1,2,3,0,1,2,3])
    channel.add(result, 0, 0, 0, -6)

if __name__ == '__main__':
    main()
