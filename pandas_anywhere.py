import pandas as pd
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
from tkinter import messagebox
import os
import re
import datetime

import pandas_profiling as pdp
from multiprocessing import Process, freeze_support
from pandasgui import show

now = datetime.datetime.now()

f = 0 #ファイルが読み込みこまれたかのフラグ(0:未読み込み 1:読み込み済み)

#アプリケーション本体
class SearchWindow(tk.Frame):
    
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("500x240")
        #self.master.resizable(width=0, height=0) #windowサイズを固定
        
        self.master.title("Pandas Anywhere Ver1.0.0")
        self.pack()
        self.filePath = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.pw_main = ttk.PanedWindow(self.master, orient="vertical")
        self.pw_main.pack(expand=True, fill=tk.BOTH, side="left")
        
        self.pw_top = ttk.PanedWindow(self.pw_main, orient="vertical", height=40)
        self.pw_main.add(self.pw_top)
        
        self.pw_middle1 = ttk.PanedWindow(self.pw_main, orient="vertical", height=50)
        self.pw_main.add(self.pw_middle1)
        
        self.pw_middle2 = ttk.PanedWindow(self.pw_main, orient="vertical", height=50)
        self.pw_main.add(self.pw_middle2)
        
        self.pw_bottom = ttk.PanedWindow(self.pw_main, orient="vertical", height=50)
        self.pw_main.add(self.pw_bottom)

        self.create_input_frame(self.pw_top)
        self.create_input_frame2(self.pw_middle1)
        self.create_input_frame3(self.pw_middle2)
        self.create_input_frame4(self.pw_bottom)
        
    def create_input_frame(self, parent):        
        fm_input = ttk.Frame(parent, )
        parent.add(fm_input)
        
        self.rb_var = tk.StringVar()
        self.rb_var.set('cp932')
        
        lbl_keyword = ttk.Label(fm_input, text="■ Select encoding format :", width=25)
        lbl_keyword.grid(row=0,column=0, padx=5, pady=10)
        
        self.rb1 = ttk.Radiobutton(fm_input, text="cp932",variable=self.rb_var,value='cp932')
        self.rb1.grid(row=0,column=1, padx=5, pady=10,sticky=tk.W)
        
        self.rb2 = ttk.Radiobutton(fm_input, text="utf-8",variable=self.rb_var,value='utf-8')
        self.rb2.grid(row=0,column=2, padx=5, pady=10,sticky=tk.W)

    def create_input_frame2(self, parent):        
        fm_input = ttk.Frame(parent, )
        parent.add(fm_input)
        
        vcmd1 = (self.master.register(self.validate_text), '%P','%S','%W') #入力値検証の変数
        
        self.entry = tk.IntVar()
        self.entry.set(1)
        
        lbl_keyword2 = ttk.Label(fm_input, text="■ Line number to start reading :", width=25)
        lbl_keyword2.grid(row=0,column=0, padx=5, pady=10,sticky=tk.W)
        
        self.ent_keyword = ttk.Entry(fm_input, justify="left", textvariable=self.entry,width=10, validate='key', validatecommand=vcmd1)
        self.ent_keyword.grid(row=0, column=1, padx=5, pady=10,sticky=tk.W)        

    def create_input_frame3(self, parent):
        fm_input = ttk.Frame(parent, )
        parent.add(fm_input)
        filepathEntry = ttk.Entry(fm_input,textvariable=self.filePath,width=40)
        filepathEntry.grid(row=0,column=0, padx=10, pady=10) 
        filepathButton = ttk.Button(fm_input,text=" Load File ",command=self.openFileDialog)
        filepathButton.grid(row=0,column=1, padx=5, pady=10)     
 
    def create_input_frame4(self, parent):
        fm_input = ttk.Frame(parent, )
        parent.add(fm_input)
        
        style = ttk.Style()
        style.configure("blue.TButton",background='SteelBlue1')
        
        outputButton = ttk.Button(fm_input,text="PandasGUI",style="blue.TButton",command=self.show_gui)
        outputButton.grid(row=1,column=1, padx=10, pady=10) 
        outputButton2 = ttk.Button(fm_input,text=" Pandas-Profilng ",style="blue.TButton",command=self.profiling)
        outputButton2.grid(row=1,column=2, padx=5, pady=10)  

    def set_data(self):
        self.enc = self.rb_var.get()
        self.skiprows = int(self.ent_keyword.get()) - 1
        print('Encoding:{}'.format(self.enc))
        print('Line number to start reading:{}'.format(self.skiprows+1))
        
    def openFileDialog(self): #ファイルを読み込む
        """
        ファイルダイアログを開く

        """
        
        self.set_data() #エンコード形式、読み込み開始行を呼び出し
        
        file  = filedialog.askopenfilename(filetypes=[("csv", "*.csv"),("txt","*.txt")]);
        
        self.file = file
        self.filePath.set(file)
         
        if file is None:         
            messagebox.showerror("load_file","File loading failure")
        else:
            if self.file[-3:] == 'csv':
                df = pd.read_csv(file, encoding=self.enc,skiprows=self.skiprows)
            else:
                df = pd.read_table(file, encoding=self.enc,skiprows=self.skiprows)
            
            self.data = df
            
            global f
        
            f = 1 #ファイル読み込みフラグ            
            
            messagebox.showinfo("Load_File","File is loaded")

    #PnadasGUI
    def show_gui(self):
        global f
        
        if f == 0: #ファイルが読み込まれていない場合      
            messagebox.showerror("Warning","File is not loading")
        else:
            gui = show(self.data)

    #pandas-profiling
    def profiling(self):
        global f
        
        if f == 0: #ファイルが読み込まれていない場合      
            messagebox.showerror("Warning","File is not loading")
        else:
            profile = pdp.ProfileReport(self.data)
            profile.to_file("profile_report" + now.strftime('_%Y%m%d_%H%M') + ".html")
            messagebox.showinfo("Pandas-Profilng","End of profiling")
            
    def validate_text(self, after, newtext, widget): #入力バリデーションの設定
        # 正規表現で入力された値が半角数字であるか判定
        if re.match(re.compile('[0-9]+'), newtext):
            # 入力された数字が1以上の場合にのみTrueを返し、数字が入力出来る
            if len(after) <= 2: 
                if after != '0':
                    return True
            return False
        # 該当しなかった場合にはFalseが返され、値はentryに反映されない
        else:
            return False
            
def main():
    root = tk.Tk()
    app = SearchWindow(master=root)
    app.mainloop()

if __name__ == "__main__":
    freeze_support()
    
    main()