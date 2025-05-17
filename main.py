from logging import root
import pandas as pd
import numpy as np
from math import log2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

from Bayes import add_new_row, create_input_fields, create_table
from DecisionTree import ID3, draw_tree_matplotlib
from KMean import KMeans

def DecisionTree():
    df = pd.read_excel("data.xlsx")
    attrs = df.columns[:-1].tolist()
    tgt = df.columns[-1]
    tree = ID3(df, tgt, attrs)
    draw_tree_matplotlib(tree)

def Bayes():
    data = [
        [1, "sunny", "hot", "high", "weak", "no"],
        [2, "sunny", "hot", "high", "strong", "no"],
        [3, "overcast", "hot", "high", "weak", "yes"],
        [4, "rainy", "mild", "high", "weak", "yes"],
        [5, "rainy", "cool", "normal", "weak", "yes"],
        [6, "rainy", "cool", "normal", "strong", "no"],
        [7, "overcast", "cool", "normal", "strong", "yes"],
        [8, "sunny", "mild", "high", "weak", "no"],
        [9, "sunny", "cool", "normal", "weak", "yes"],
        [10, "rainy", "mild", "normal", "weak", "yes"],
        [11, "sunny", "mild", "normal", "strong", "yes"],
        [12, "overcast", "mild", "high", "strong", "yes"],
        [13, "overcast", "hot", "normal", "weak", "yes"],
        [14, "rainy", "mild", "high", "strong", "no"],
        [15, "sunny", "cool", "normal", "strong", "no"]
    ]

    columns = ["id", "outlook", "temperature", "humidity", "wind", "play"]
    input_columns = ["outlook", "temperature", "humidity", "wind"]

    df = pd.DataFrame(data, columns=columns)

    root = tk.Tk()
    window_width = 800
    window_height = 600

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
    root.title("Weather Play Dataset")

    tree = None
    combo_boxes = {}
    create_table(root)
    create_input_fields(root)

    btn_add = tk.Button(root, text="Confirm", command=add_new_row)
    btn_add.pack(pady=5)

def KMeanFunc():
    # Đọc dữ liệu từ file Excel
    df = pd.read_excel("data_kmeans.xlsx")

    X = df.iloc[:, 1].apply(lambda s: eval(s)).tolist()

    model = KMeans()
    k = 3
    centroids, labels = model.fit(X, k)


    colors = ['red', 'green', 'blue', 'purple', 'orange']
    plt.figure(figsize=(8, 6))

    for i in range(len(X)):
        plt.scatter(X[i][0], X[i][1], color=colors[labels[i]], alpha=0.6)

    for i, centroid in enumerate(centroids):
        plt.scatter(centroid[0], centroid[1], color=colors[i], marker='X', s=200, edgecolor='black')

    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Kết quả')
    plt.grid(True)
    plt.show()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Nhóm 2")
root.geometry("300x200")

# Tạo các nút
button1 = tk.Button(root, text="Decision Tree", command=DecisionTree, width=20)
button1.pack(pady=10)

button2 = tk.Button(root, text="Bayes", command=Bayes, width=20)
button2.pack(pady=10)

button3 = tk.Button(root, text="KMean", command=KMeanFunc, width=20)
button3.pack(pady=10)

# Chạy vòng lặp giao diện
root.mainloop()