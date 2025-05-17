import math
import random
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

class KMeans:
    def __init__(self):
        pass
    #Tính khoảng cách Euclid giữa hai điểm
    def KhoangCah(self, point1, point2):
        tong = 0
        for i in range(len(point1)):
            tong += (point1[i] - point2[i]) ** 2
        return math.sqrt(tong)
    # Khởi tạo ngẫu nhiên k tâm cụm ban đầu từ danh sách các điểm:
    def TamCum(self, point, k):
        point_copy = point.copy()
        random.shuffle(point_copy)
        return point_copy[:k]
    # Trả về danh sách các nhãn labels tương ứng với cụm
    def PhamCum(self, centroids, points):
        labels = []
        for point in points:
            KhoangCachMin = float('inf')
            cluster_idx = -1
            for i, centroid in enumerate(centroids):
                KhoangCach = self.KhoangCah(point, centroid)
                if KhoangCach < KhoangCachMin:
                    KhoangCachMin = KhoangCach
                    cluster_idx = i
            labels.append(cluster_idx)
        return labels
    # Tính trung bình cộng của tất cả các điểm dữ liệu thuộc về mỗi cụm và cập nhật cụm
    def CapNhatTamCum(self, points, labels, k):
        new_centroids = []
        for cluster_idx in range(k):
            cluster_point = [points[i] for i, label in enumerate(labels) if label == cluster_idx]
            if not cluster_point:
                # Nếu cụm rỗng, chọn ngẫu nhiên một điểm trong tập dữ liệu làm tâm cụm mới
                new_centroids.append(random.choice(points))
                continue
            centroid = [sum(dim) / len(cluster_point) for dim in zip(*cluster_point)]
            new_centroids.append(centroid)
        return new_centroids

    def KiemTraHoiTu(self, old_centroids, new_centroids, old_labels, new_labels, tol=1e-4):
        total_distance = 0
        for i in range(len(old_centroids)):
            distance = self.KhoangCah(old_centroids[i], new_centroids[i])
            total_distance += distance
        if Counter(old_labels) != Counter(new_labels):
            return False
        return total_distance < tol

    def fit(self, X, k, max_iter=100, init_centroids=None):
        if init_centroids is None:
            centroids = self.TamCum(X, k)
        else:
            centroids = init_centroids
        print("Tâm cụm ban đầu:")
        if len(X)==0:
            raise ValueError("Tập dữ liệu rỗng")
        if k<=0:
            raise ValueError("Số cụm phải lớn hơn 0")
        if k>len(X):
            raise ValueError("Số cụm không thể lớn hơn số lượng điểm dữ liệu")
        for i, c in enumerate(centroids):
            print(f"  Cụm {i}: {c}")

        for it in range(max_iter):
            print(f"\n--- Vòng lặp {it+1} ---")
            labels = self.PhamCum(centroids, X)
            new_labels = self.PhamCum(centroids, X)
            for i, point in enumerate(X):
                print(f"Điểm {point} -> Cụm {labels[i]}")

            new_centroids = self.CapNhatTamCum(X, labels, k)
            for i, c in enumerate(new_centroids):
                print(f"  Tâm cụm {i} cập nhật: {c}")

            if self.KiemTraHoiTu(centroids, new_centroids, labels, new_labels):
                print("\n>>> Hội tụ. Kết thúc.")
                break
            centroids = new_centroids
            labels= new_labels

        return centroids, labels