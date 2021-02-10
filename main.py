from PIL import Image
from lfsr import LFSR
from functools import reduce
from feedback import feedback_poly, one_hot_encode

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import sys

class MainWindow:
    """ GUI Wrapper """

    # configure root directory path relative to this file
    THIS_FOLDER_G = ""
    if getattr(sys, "frozen", False):
        # frozen
        THIS_FOLDER_G = os.path.dirname(sys.executable)
    else:
        # unfrozen
        THIS_FOLDER_G = os.path.dirname(os.path.realpath(__file__))

    def __init__(self, root):
        self.root = root
        self._file_url = tk.StringVar()
        self._secret_key = tk.StringVar()
        self._salt = tk.StringVar()
        self._status = tk.StringVar()
        self._status.set("")

        self.should_cancel = False

        root.title("โปรแกรมการเข้ารหัสและถอดรหัสแบบ LFSR")
        root.configure(bg="#eeeeee")


        try:
            icon_img = tk.Image(
                "photo",
                file=self.THIS_FOLDER_G + "/assets/icon.png"
            )
            root.call(
                "wm",
                "iconphoto",
                root._w,
                icon_img
            )
        except Exception:
            pass

        self.menu_bar = tk.Menu(
            root,
            bg="#eeeeee",
            relief=tk.FLAT
        )
        self.menu_bar.add_command(
            label="วิธีการใช้งาน",
            command=self.show_help_callback
        )
        self.menu_bar.add_command(
            label="ออกจากโปรแกรม!",
            command=root.quit
        )

        root.configure(
            menu=self.menu_bar
        )

        self.file_entry_label = tk.Label(
            root,
            text="กรุณาใส่ที่อยู่ของไฟล์รูป หรือ เลือกไฟล์รูปที่ปุ่มเลือกไฟล์ได้",
            bg="#eeeeee",
            anchor=tk.W,
            font='bold, 10'

        )
        self.file_entry_label.grid(
            padx=12,
            pady=(8, 0),
            ipadx=0,
            ipady=1,
            row=0,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.file_entry = tk.Entry(
            root,
            textvariable=self._file_url,
            bg="#fff",
            exportselection=0,
            relief=tk.FLAT
        )
        self.file_entry.grid(
            padx=15,
            pady=6,
            ipadx=8,
            ipady=8,
            row=1,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.select_btn = tk.Button(
            root,
            text="เลือกไฟล์รูป",
            command=self.selectfile_callback,
            width=42,
            bg="#000080",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT,
            font="10"
        )
        self.select_btn.grid(
            padx=15,
            pady=8,
            ipadx=24,
            ipady=6,
            row=2,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        # self.key_entry_label = tk.Label(
        #     root,
        #     text="LFSR = Length 1-15",
        #     bg="#eeeeee",
        #     anchor=tk.W
        # )
        # self.key_entry_label.grid(
        #     padx=12,
        #     pady=(8, 0),
        #     ipadx=0,
        #     ipady=1,
        #     row=3,
        #     column=0,
        #     columnspan=4,
        #     sticky=tk.W+tk.E+tk.N+tk.S
        # )

        # self.key_entry = tk.Entry(
        #     root,
        #     textvariable=self._secret_key,
        #     bg="#fff",
        #     exportselection=0,
        #     relief=tk.FLAT
        # )
        # self.key_entry.grid(
        #     padx=15,
        #     pady=6,
        #     ipadx=8,
        #     ipady=8,
        #     row=4,
        #     column=0,
        #     columnspan=4,
        #     sticky=tk.W+tk.E+tk.N+tk.S
        # )

        self.encrypt_btn = tk.Button(
            root,
            text="เข้ารหัสไฟล์รูป",
            command=self.encrypt_callback,
            bg="#ed3833",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT,
            font="10"
        )
        self.encrypt_btn.grid(
            padx=(15, 6),
            pady=8,
            ipadx=24,
            ipady=6,
            row=7,
            column=0,
            columnspan=2,
            sticky=tk.W+tk.E+tk.N+tk.S
        )
        
        self.decrypt_btn = tk.Button(
            root,
            text="ถอดรหัสไฟล์รูป",
            command=self.decrypt_callback,
            bg="#00bd56",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT,
            font="10"
        )
        self.decrypt_btn.grid(
            padx=(6, 15),
            pady=8,
            ipadx=24,
            ipady=6,
            row=7,
            column=2,
            columnspan=2,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.reset_btn = tk.Button(
            root,
            text="ล้างข้อมูล",
            command=self.reset_callback,
            bg="#aaaaaa",
            fg="#ffffff",
            bd=2,
            relief=tk.FLAT,
            font="10"
        )
        self.reset_btn.grid(
            padx=15,
            pady=(4, 12),
            ipadx=24,
            ipady=6,
            row=8,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        self.status_label = tk.Label(
            root,
            textvariable=self._status,
            bg="#eeeeee",
            anchor=tk.W,
            justify=tk.LEFT,
            relief=tk.FLAT,
            wraplength=350
        )
        self.status_label.grid(
            padx=12,
            pady=(0, 12),
            ipadx=0,
            ipady=1,
            row=9,
            column=0,
            columnspan=4,
            sticky=tk.W+tk.E+tk.N+tk.S
        )

        tk.Grid.columnconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 1, weight=1)
        tk.Grid.columnconfigure(root, 2, weight=1)
        tk.Grid.columnconfigure(root, 3, weight=1)

    def selectfile_callback(self):
        try:
            name = filedialog.askopenfile()
            self._file_url.set(name.name)
            #print(name.name)
            
        except Exception as e:
            self._status.set(e)
            self.status_label.update()
    

    
    def freeze_controls(self):
        self.file_entry.configure(state="disabled")
        # self.key_entry.configure(state="disabled")
        self.select_btn.configure(state="disabled")
        self.encrypt_btn.configure(state="disabled")
        self.decrypt_btn.configure(state="disabled")
        self.reset_btn.configure(text="CANCEL", command=self.cancel_callback,
            fg="#ed3833", bg="#fafafa")
        self.status_label.update()
    
    def unfreeze_controls(self):
        self.file_entry.configure(state="normal")
        # self.key_entry.configure(state="normal")
        self.select_btn.configure(state="normal")
        self.encrypt_btn.configure(state="normal")
        self.decrypt_btn.configure(state="normal")
        self.reset_btn.configure(text="RESET", command=self.reset_callback,
            fg="#ffffff", bg="#aaaaaa")
        self.status_label.update()

    def encrypt_callback(self):        
        try:
            lfsr = LFSR(15, 'gal', [1 for _ in range(15)])
            s = ""
            ints =  lfsr.encrypt_decrypt_ints()
            value  = 0
            im = Image.open(r"{}".format(self._file_url.get()))
            px = im.load() 
            print(px[0,0])
            width, height = im.size
            print("Height :", height, " And width : ", width)
            for i in range(width):
                for j in range(height):
                    r, g, b, temp = px[i, j]
                    r = (r) ^ ints[value]
                    value = (value+1) % (len(ints))
                    g = (g) ^ ints[value]
                    value = (value+1)%(len(ints))
                    b = (b) ^ ints[value]
                    value = (value+1) % (len(ints))
                    temp = (temp) ^ ints[value]
                    value = (value+1) % (len(ints))
                    px[i, j] = (r, g, b, temp)
            im.show()   
            im.save(r"D:\สำรองงาน desktop\ไฟล์งานเทอม 1.1 ปี 3\อ.บาส\project อ.บาส\LFSR Algorithm\image\encrytion.png")
            
            self._status.set("ทำการเข้ารหัสรูปภาพเรียบร้อย!")
            
            if self.should_cancel:
                #self._cipher.abort()
                self._status.set("Cancelled!")
            #self._cipher = None
            self.should_cancel = False
        except Exception as e:
            # print(e)
            self._status.set(e)

        self.unfreeze_controls()

    def decrypt_callback(self):
        try:
            lfsr = LFSR(15, 'gal', [1 for _ in range(15)])
            s = ""
            ints =  lfsr.encrypt_decrypt_ints()
            value  = 0
            im = Image.open(r"{}".format(self._file_url.get()))
            px = im.load()
            width, height = im.size
            print("Height :", height, " And width : ", width)
            for i in range(width):
                for j in range(height):
                    r, g, b, temp = px[i, j]
                    r = (r) ^ ints[value]
                    value = (value+1) % (len(ints))
                    g = (g) ^ ints[value]
                    value = (value+1)%(len(ints))
                    b = (b) ^ ints[value]
                    value = (value+1) % (len(ints))
                    temp = (temp) ^ ints[value]
                    value = (value+1) % (len(ints))
                    px[i, j] = (r, g, b, temp)

            im.show()
            im.save(r"D:\สำรองงาน desktop\ไฟล์งานเทอม 1.1 ปี 3\อ.บาส\project อ.บาส\LFSR Algorithm\image\decrytion.png")        
            self._status.set("ทำการถอดรหัสรูปภาพเรียบร้อย!!")

            if self.should_cancel:
                #self._cipher.abort()
                self._status.set("Cancelled!")
            #self._cipher = None
            self.should_cancel = False
        except Exception as e:
            # print(e)
            self._status.set(e)
        
        self.unfreeze_controls()

    def reset_callback(self):
        self._cipher = None
        self._file_url.set("")
        self._secret_key.set("")
        self._salt.set("")
        self._status.set("---")
    
    def cancel_callback(self):
        self.should_cancel = True

    def show_help_callback(self):
        messagebox.showinfo(
            "How To",
            """1. เปิดแอพและคลิกปุ่มเลือกไฟล์แล้วเลือกไฟล์ของคุณเช่น "อิอิ.jpg"
2. คลิกปุ่ม ENCRYPT เพื่อเข้ารหัส
3. เมื่อคุณต้องการถอดรหัสไฟล์คุณจะเลือกไฟล์ที่มีชื่อว่า Encrypt จากนั้นคลิกปุ่ม DECRYPT เพื่อถอดรหัส .
4. ได้รูปภาพที่ทำการถอดรหัสเรียบร้อย."""
        )


if __name__ == "__main__":
    ROOT = tk.Tk()
    MAIN_WINDOW = MainWindow(ROOT)
    ROOT.mainloop()
