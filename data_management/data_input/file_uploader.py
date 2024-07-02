import pandas as pd


def read_csv(file_path):
    """读取 CSV 文件并返回数据帧"""
    return pd.read_csv(file_path)