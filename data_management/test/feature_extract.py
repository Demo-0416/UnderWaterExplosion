import numpy as np
from scipy.signal import find_peaks
from scipy.fft import fft
from scipy.integrate import simpson
from scipy import stats

def extract_peak_value(data):
    """
    提取峰值
    """
    peaks, _ = find_peaks(data)
    return data[peaks].max()

def extract_time_constant(data, fs):
    """
    提取时间常数
    """
    return np.exp(-1/fs) * np.sum(data)

def extract_specific_impulse(data, fs):
    """
    提取比冲击波能
    """
    return simpson(data, dx=1/fs)

def extract_specific_impulse_momentum(data, fs):
    """
    提取比冲量
    """
    return np.trapz(data, dx=1/fs)

def extract_energy_spectrum(data, fs):
    """
    提取能量谱
    """
    N = len(data)
    yf = fft(data)
    xf = np.fft.fftfreq(N, 1/fs)
    return np.abs(yf[:N//2])**2

def extract_energy(data, fs):
    """
    提取能量
    """
    return simpson(data**2, dx=1/fs)

def extract_pulsation_period(data, fs):
    """
    提取脉动周期
    """
    peaks, _ = find_peaks(data)
    if len(peaks) > 1:
        return np.mean(np.diff(peaks)) / fs
    else:
        return np.nan

def extract_max_negative_value(data):
    """
    提取最大负值
    """
    return data.min()

def extract_plastic_strain(data):
    """
    提取塑性应变值
    """
    return np.max(data) - np.min(data)

def extract_peak_strain(data):
    """
    提取峰值应变
    """
    return np.max(data)

def extract_max_strain(data):
    """
    提取最大应变
    """
    return np.max(data)

def time_frequency_transform(data, fs):
    """
    时频变换 (Short Time Fourier Transform)
    """
    from scipy.signal import stft
    f, t, Zxx = stft(data, fs)
    return f, t, np.abs(Zxx)

def extract_energy_spectrum_strain(data, fs):
    """
    应变能量谱计算
    """
    return extract_energy_spectrum(data, fs)

def extract_statistical_values(data):
    """
    提取统计值
    """
    mean = np.mean(data)
    std_dev = np.std(data)
    skewness = stats.skew(data)
    kurtosis = stats.kurtosis(data)
    return mean, std_dev, skewness, kurtosis

def extract_shock_spectrum(data, fs):
    """
    冲击谱计算
    """
    from scipy.signal import find_peaks
    
    def compute_shock_response_spectrum(acceleration, fs):
        # This is a placeholder function; replace with actual shock spectrum computation
        peaks, _ = find_peaks(acceleration)
        spectrum = acceleration[peaks]
        return spectrum
    
    return compute_shock_response_spectrum(data, fs)

# # 示例信号
# fs = 1000  # 采样率
# t = np.linspace(0, 1, fs)
# data = np.sin(2 * np.pi * 5 * t) + np.random.normal(0, 0.1, fs)

# # 自由场压力/壁压数据特征提取
# peak_value = extract_peak_value(data)
# time_constant = extract_time_constant(data, fs)
# specific_impulse = extract_specific_impulse(data, fs)
# specific_impulse_momentum = extract_specific_impulse_momentum(data, fs)
# energy_spectrum = extract_energy_spectrum(data, fs)
# energy = extract_energy(data, fs)
# pulsation_period = extract_pulsation_period(data, fs)
# max_negative_value = extract_max_negative_value(data)

# print("峰值:", peak_value)
# print("时间常数:", time_constant)
# print("比冲击波能:", specific_impulse)
# print("比冲量:", specific_impulse_momentum)
# print("能量谱:", energy_spectrum)
# print("能量:", energy)
# print("脉动周期:", pulsation_period)
# print("最大负值:", max_negative_value)

# # 应变数据特征提取
# plastic_strain = extract_plastic_strain(data)
# peak_strain = extract_peak_strain(data)
# max_strain = extract_max_strain(data)
# frequencies, times, Zxx = time_frequency_transform(data, fs)
# energy_spectrum_strain = extract_energy_spectrum_strain(data, fs)

# print("塑性应变值:", plastic_strain)
# print("峰值应变:", peak_strain)
# print("最大应变:", max_strain)
# print("时频变换频率:", frequencies)
# print("时频变换时间:", times)
# print("时频变换幅值:", Zxx)
# print("应变能量谱:", energy_spectrum_strain)

# # 加速度数据特征提取
# mean, std_dev, skewness, kurtosis = extract_statistical_values(data)
# shock_spectrum = extract_shock_spectrum(data, fs)

# print("统计值 - 平均值:", mean)
# print("统计值 - 标准差:", std_dev)
# print("统计值 - 偏度:", skewness)
# print("统计值 - 峰度:", kurtosis)
# print("冲击谱:", shock_spectrum)



