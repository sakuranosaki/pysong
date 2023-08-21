import math

WAV_FREQ = 44100

def ratio_from_gain(gain):
    return math.pow(10, gain / 20)

def biquad_equalizer(data, freq, q, gain):
    a = math.pow(10, gain / 40)
    w0 = 2 * math.pi * freq / WAV_FREQ
    alpha = math.sin(w0) / (2 * q)
    b0 = 1 + alpha * a
    b1 = -2 * math.cos(w0)
    b2 = 1 - alpha * a
    a0 = 1 + alpha / a
    a1 = -2 * math.cos(w0)
    a2 = 1 - alpha / a

    out = []
    for i in range(0, len(data)):
        if i < 2:
            out.append(data[i])
        else:
            out.append((b0 / a0) * data[i] + (b1 / a0) * data[i-1] + (b2 / a0) * data[i-2] - (a1 / a0) * out[i-1] - (a2 / a0) * out[i-2])
    return out

def biquad_lowpass(data, freq, q):
    w0 = 2 * math.pi * freq / WAV_FREQ
    alpha = math.sin(w0) / (2 * q)
    b0 = (1 - math.cos(w0)) / 2
    b1 = 1 - math.cos(w0)
    b2 = (1 - math.cos(w0)) / 2
    a0 = 1 + alpha
    a1 = -2 * math.cos(w0)
    a2 = 1 - alpha

    out = []
    for i in range(0, len(data)):
        if i < 2:
            out.append(data[i])
        else:
            out.append((b0 / a0) * data[i] + (b1 / a0) * data[i-1] + (b2 / a0) * data[i-2] - (a1 / a0) * out[i-1] - (a2 / a0) * out[i-2])
    return out

def soft_limit(data, threshold_gain):
    out = []
    r = ratio_from_gain(threshold_gain)
    for i in range(0, len(data)):
        out.append(math.tanh(data[i] / r) * r)
    return out
