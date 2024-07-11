import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pywt
from scipy.optimize import curve_fit
from scipy.signal import medfilt

def fir_filter(input_signal, numtaps, cutoff, fs, window='hamming'):
    """
    FIR滤波器

    参数:
    input_signal - 输入信号
    numtaps - 滤波器阶数
    cutoff - 截止频率
    fs - 采样率
    window - 窗函数类型（默认为'Hamming'）

    返回:
    filtered_signal - 经过滤波后的信号
    """
    # 设计 FIR 滤波器系数
    taps = signal.firwin(numtaps, cutoff, window=window, fs=fs)
    
    # 应用 FIR 滤波器
    filtered_signal = signal.lfilter(taps, 1.0, input_signal)
    
    return filtered_signal

def iir_filter(input_signal, order, cutoff, fs, btype='low'):
    """
    IIR滤波器

    参数:
    input_signal - 输入信号
    order - 滤波器阶数
    cutoff - 截止频率
    fs - 采样率
    btype - 滤波器类型（默认为'low'）

    返回:
    filtered_signal - 经过滤波后的信号
    """
    # 设计 IIR 滤波器系数
    b, a = signal.butter(order, cutoff, btype=btype, analog=False, fs=fs)
    
    # 应用 IIR 滤波器
    filtered_signal = signal.lfilter(b, a, input_signal)
    
    return filtered_signal

def wavelet_transform(input_signal, wavelet='db1', level=1):
    """
    小波变换

    参数:
    input_signal - 输入信号
    wavelet - 小波函数（默认为'db1'）
    level - 分解层数（默认为1）

    返回:
    coeffs - 小波变换系数

    # 应用小波变换
coeffs = wavelet_transform(input_signal, wavelet, level)

    # 重构信号（从小波系数）
reconstructed_signal = pywt.waverec(coeffs, wavelet)
    """
    coeffs = pywt.wavedec(input_signal, wavelet, level=level)
    return coeffs


def moving_average(input_signal, window_size):
    """
    滑动平均

    参数:
    input_signal - 输入信号
    window_size - 窗口大小

    返回:
    smoothed_signal - 经过平滑处理的信号
    """
    window = np.ones(int(window_size))/float(window_size)
    smoothed_signal = np.convolve(input_signal, window, 'same')
    return smoothed_signal

def polynomial_fit(x, y, degree):
    """
    多项式拟合

    参数:
    x - 自变量数据
    y - 因变量数据
    degree - 多项式阶数

    返回:
    p - 多项式系数
    y_fit - 拟合后的值
    """
    p = np.polyfit(x, y, degree)
    y_fit = np.polyval(p, x)
    return p, y_fit

def exponential_fit(x, y):
    """
    指数拟合

    参数:
    x - 自变量数据
    y - 因变量数据

    返回:
    popt - 拟合参数
    y_fit - 拟合后的值
    """
    def exp_func(x, a, b, c):
        return a * np.exp(b * x) + c
    
    popt, pcov = curve_fit(exp_func, x, y)
    y_fit = exp_func(x, *popt)
    return popt, y_fit

def median_filter(input_signal, kernel_size):
    """
    中值滤波

    参数:
    input_signal - 输入信号
    kernel_size - 滤波器窗口大小

    返回:
    filtered_signal - 经过滤波后的信号
    """
    filtered_signal = medfilt(input_signal, kernel_size=kernel_size)
    return filtered_signal

def frequency_domain_filter(input_signal, cutoff, fs):
    """
    频域滤波

    参数:
    input_signal - 输入信号
    cutoff - 截止频率
    fs - 采样率

    返回:
    filtered_signal - 经过滤波后的信号
    """
    # 傅里叶变换
    freq_signal = np.fft.fft(input_signal)
    freq = np.fft.fftfreq(len(input_signal), d=1/fs)
    
    # 设计低通滤波器
    filter_mask = np.abs(freq) < cutoff
    freq_signal_filtered = freq_signal * filter_mask
    
    # 逆傅里叶变换
    filtered_signal = np.fft.ifft(freq_signal_filtered)
    
    return np.real(filtered_signal)

