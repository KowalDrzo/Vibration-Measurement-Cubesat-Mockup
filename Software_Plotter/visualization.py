from frame import Frame

import matplotlib.pyplot as plt
import numpy as np

class Visulization:

    def __init__(self, filename):

        frames = []
        scale = 1
        content = ""
        with open(filename) as file:
            scale = float(file.readline())
            content = file.readlines()

        time_base = 0
        for line in content:
            
            frame = Frame()
            frame.time_us = time_base
            frame.x, frame.y, frame.z = map(int, line.split(";"))
            frames.append(frame)
            time_base += 0.0001

        t = []
        x = []
        y = []
        z = []

        for frame in frames:
            t.append(frame.time_us)
            x.append(frame.x)
            y.append(frame.y)
            z.append(frame.z)

        # Remove constant part:
        x = x - np.mean(x)
        y = y - np.mean(y)
        z = z - np.mean(z)

        # Change raw adc value to acceleration:
        # For VSA004 0.304 and for ADXL 0.647.
        for i in range(len(x)):
            x[i] *= scale
            y[i] *= scale
            z[i] *= scale

        # sampling rate 10 kHz:
        sr = 10000
        # sampling interval:
        ts = 1.0/sr

        X = np.fft.fft(x)
        Y = np.fft.fft(y)
        Z = np.fft.fft(z)
        N = len(X)
        n = np.arange(N)
        T = N/sr
        freq = n/T

        # Normalize FFT values:
        for i in range(N):
            X[i] /= N
            Y[i] /= N
            Z[i] /= N

        # Generate plots:
        plt.figure(figsize=(12, 6))

        # Time signal:
        plt.subplot(2, 1, 1)
        plt.plot(t, x)
        plt.plot(t, y)
        plt.plot(t, z)
        plt.title('x(t)')
        plt.xlabel('Czas [s]')
        plt.ylabel('Amplituda [g]')

        # FFT plot:
        plt.subplot(2, 1, 2)
        plt.plot(freq, np.abs(X))
        plt.plot(freq, np.abs(Y))
        plt.plot(freq, np.abs(Z))
        plt.title('x(f)')
        plt.xlabel('Częstotliwość [Hz]')
        plt.ylabel('PDS [g^2/Hz]')
        plt.xlim(-10, 5000)

        plt.tight_layout()
        plt.show()
