import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

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



tree = None
combo_boxes = {}

def create_table(root):
    global tree
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor = "center")
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    refresh_table()

def refresh_table():
    tree.delete(*tree.get_children())
    for row in df.itertuples(index=False):
        tree.insert("", tk.END, values=row)

def create_input_fields(root):
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    for col in input_columns:
        frame = tk.Frame(input_frame)
        frame.pack(side=tk.LEFT, padx=5)
        lbl = tk.Label(frame, text=col)
        lbl.pack()
        values = sorted(df[col].unique().tolist())
        combo = ttk.Combobox(frame, values=values, state="readonly")
        combo.pack()
        combo_boxes[col] = combo
        
def bayes_function(input):
    x_str = "X("
    for i, inp in enumerate(input):
        x_str = x_str + inp
        if(i == (len(input)-1)):
            x_str = x_str + ")"
        else:
            x_str = x_str + ","
    print(x_str)
        
    total = len(df)
    
    yes_count = df[df["play"] == "yes"].shape[0]
    no_count = df[df["play"] == "no"].shape[0]
    yes_percentage = yes_count / total
    no_percentage = no_count / total
    
    x_yes_percentage = 1
    x_no_percentage = 1
    
    for i, atr in enumerate(input_columns):
        atr_yes_count = df[(df[atr] == input[i]) & (df["play"] == "yes")].shape[0]
        atr_no_count = df[(df[atr] == input[i]) & (df["play"] == "no")].shape[0]
        atr_yes_percentage = atr_yes_count / yes_count
        atr_no_percentage = atr_no_count / no_count
        x_yes_percentage = x_yes_percentage * atr_yes_percentage
        x_no_percentage = x_no_percentage * atr_no_percentage
        print("P({} = {}| play = yes) = {}".format(atr, input[i], str(atr_yes_percentage)))
        print("P({} = {}| play = no) = {}".format(atr, input[i], str(atr_no_percentage)))
        
    print("P(X| play = yes) = {}".format(x_yes_percentage))
    print("P(X| play = no) = {}".format(x_no_percentage))
    
    yes_score = x_yes_percentage * yes_percentage
    no_score = x_no_percentage * no_percentage
    
    print("P(X| play = yes) * P(X| play = yes) = {}".format(yes_score))
    print("P(X| play = no) * P(X| play = no) = {}".format(no_score))
    
    if(yes_score >= no_score):
        print("X thuộc nhóm play = yes")
        return "yes"
    print("X thuộc nhóm play = no")
    return "no"
    

def add_new_row():
    global df
    new_id = df["id"].max() + 1 if not df.empty else 1
    new_data = []
    input = []
    for col in input_columns:
        val = combo_boxes[col].get()
        input.append(val)
        if val == "":
            raise ValueError(f"Chưa chọn giá trị cho '{col}'")
        new_data.append(val)

    play_value = bayes_function(input)
    new_row = [new_id] + new_data + [play_value]
    df.loc[len(df)] = new_row
    refresh_table()

    for cb in combo_boxes.values():
        cb.set("")

# create_table()
# create_input_fields()

# btn_add = tk.Button(root, text="Confirm", command=add_new_row)
# btn_add.pack(pady=5)

# root.mainloop()
