import pandas as pd
import numpy as np
from math import log2
import matplotlib.pyplot as plt

# --- Hàm tính Entropy và Info Gain ---
# Tính entropy của một tập nhãn
def entropy(labels):
    values, counts = np.unique(labels, return_counts=True)
    probs = counts / counts.sum()
    return -np.sum(probs * np.log2(probs))

# Tính tổng entropy, entropy có trọng số, và thông tin thu được (information gain)
def info_gain(df, attribute, target_attr):
    total_entropy = entropy(df[target_attr])
    vals, counts = np.unique(df[attribute], return_counts=True)
    weighted_entropy = sum(
        (counts[i] / counts.sum()) * entropy(df[df[attribute] == vals[i]][target_attr])
        for i in range(len(vals))
    )
    return total_entropy, weighted_entropy, total_entropy - weighted_entropy

# --- Thuật toán ID3 xây dựng cây quyết định ---
# Xây dựng cây theo thuật toán ID3 và in ra quá trình lựa chọn thuộc tính

def ID3(df, target_attr, attributes, default_class=None, depth=0):
    indent = "  " * depth

    # Trường hợp tập dữ liệu rỗng
    if len(df) == 0:
        print(f"{indent}Tập rỗng → return mặc định: {default_class}")
        return default_class

    # Trường hợp tất cả các mẫu đều cùng một lớp
    if len(np.unique(df[target_attr])) == 1:
        label = np.unique(df[target_attr])[0]
        print(f"{indent}Tất cả cùng 1 lớp → return: {label}")
        return label

    # Trường hợp không còn thuộc tính nào để phân nhánh
    if not attributes:
        majority = df[target_attr].mode()[0]
        print(f"{indent}Không còn thuộc tính → return nhãn đa số: {majority}")
        return majority

    # Xác định class mặc định là nhãn chiếm đa số
    default_class = df[target_attr].mode()[0]
    total_entropy = entropy(df[target_attr])
    print(f"{indent}Info(D) = {total_entropy:.4f}")

    infos = []
    gains = []
    for attr in attributes:
        _, info, gain = info_gain(df, attr, target_attr)
        infos.append(info)
        gains.append(gain)
        print(f"{indent}  {attr}: Info = {info:.4f}, Gain = {gain:.4f}")

    # Chọn thuộc tính có thông tin thu được lớn nhất
    best_attr_index = np.argmax(gains)
    best_attr = attributes[best_attr_index]
    print(f"{indent}--> Chọn thuộc tính '{best_attr}' để phân nhánh\n")

    # Tạo node gốc với thuộc tính tốt nhất và đệ quy
    tree = {best_attr: {}}
    for val in np.unique(df[best_attr]):
        print(f"{indent}Nhánh {best_attr} = {val}:")
        subset = df[df[best_attr] == val]
        subtree = ID3(subset, target_attr, [a for a in attributes if a != best_attr], default_class, depth + 1)
        tree[best_attr][val] = subtree
    return tree

# --- Vẽ cây quyết định bằng matplotlib ---
# Lớp đại diện cho một node trong cây
class TreeNode:
    def __init__(self, name, is_leaf=False):
        self.name = name
        self.is_leaf = is_leaf
        self.children = []

# Chuyển cây dạng dictionary sang dạng đối tượng TreeNode để vẽ

def dict_to_tree(d):
    if not isinstance(d, dict):
        return TreeNode(f"Class: {d}", is_leaf=True)
    attr = next(iter(d))
    node = TreeNode(attr)
    for edge, subtree in d[attr].items():
        child = dict_to_tree(subtree)
        node.children.append((edge, child))
    return node

# Bố trí vị trí các node trong cây để vẽ

def layout(node, depth=0, positions=None, edges=None, counter=None, y_step=0.15):
    if positions is None:
        positions, edges, counter = {}, {}, {'x':0}
    y = 1 - depth * y_step
    if node.is_leaf:
        x = counter['x']
        counter['x'] += 1
        positions[node] = (x, y)
    else:
        xs = []
        for label, child in node.children:
            layout(child, depth+1, positions, edges, counter, y_step)
            edges[(node, child)] = label
            xs.append(positions[child][0])
        x = sum(xs) / len(xs)
        positions[node] = (x, y)
    return positions, edges

# Vẽ cây quyết định bằng matplotlib

def draw_tree_matplotlib(tree_dict, title="Decision Tree", figsize=(12,8)):
    root = dict_to_tree(tree_dict)
    positions, edges = layout(root)
    xs = [pos[0] for pos in positions.values()]
    min_x, max_x = min(xs), max(xs)
    span = max_x - min_x or 1
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_axis_off()

    # Vẽ các cạnh nối giữa các node
    for (parent, child), label in edges.items():
        x0, y0 = positions[parent]
        x1, y1 = positions[child]
        ax.annotate('', xy=((x1-min_x)/span, y1), xytext=((x0-min_x)/span, y0), arrowprops=dict(arrowstyle='->'))
        mx, my = ((x0+x1)/2 - min_x)/span, (y0+y1)/2
        ax.text(mx, my, str(label), ha='center', va='center', bbox=dict(facecolor='yellow', boxstyle='round,pad=0.2'))

    # Vẽ các node (hình tròn cho lá, hình tròn xanh cho nhãn)
    for node, (x, y) in positions.items():
        xn = (x - min_x) / span
        if node.is_leaf:
            ax.text(xn, y, node.name, ha='center', va='center', bbox=dict(facecolor='lightgreen', boxstyle='circle'))
        else:
            ax.text(xn, y, node.name + '?', ha='center', va='center', bbox=dict(facecolor='lightblue', boxstyle='round'))

    ax.set_title(title)
    plt.tight_layout()
    plt.show()

# Đọc dữ liệu từ file Excel, xác định các thuộc tính và nhãn mục tiêu
'''
df = pd.read_excel("data.xlsx")
attrs = df.columns[:-1].tolist()
tgt = df.columns[-1]
tree = ID3(df, tgt, attrs)
#print("Cây quyết định:",tree)
draw_tree_matplotlib(tree)
'''