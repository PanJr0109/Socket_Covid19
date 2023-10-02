import socket
import sys
import tkinter as tk
from tkinter import Frame, Label, messagebox
from tkinter import ttk
import tkinter
from tkinter import *
from tkinter.ttk import Combobox


LOGIN = "login"
LOGOUT = "logout"
SIGNUP = "signup"
EXIT = "out"
SEARCH = "search"
FONT = ("timenewroman", 15, "bold")
idx = 0


COUNTRY=["World","USA","India","Brazil","UK","Russia","France","Turkey","Germany","Iran","Spain","Italy","Argentina","Colombia","Indonesia","Poland","Mexico","Ukraine","South Africa","Netherlands","Philippines","Malaysia","Czechia","Peru","Thailand","Canada","Iraq","Belgium","Romania","Chile","Japan",
         "Vietnam","Bangladesh","Israel","Portugal","Sweden","Serbia","Pakistan","Switzerland","Austria","Hungary",
         "Greece","Jordan","Kazakhstan","Cuba","Morocco","Georgia","Slovakia","Nepal","Denmark","UAE","Ireland","Bulgaria",
         "Tunisia","Lebanon","Croatia","Belarus","Guatemala","S. Korea","Azerbaijan","Sri Lanka","Bolivia","Costa Rica","Saudi Arabia",
         "Ecuador","Myanmar","Lithuania","Panama","Paraguay","Slovenia","Venezuela","Palestine","Dominican Republic","Kuwait",
         "Ethiopia","Uruguay","Mongolia","Libya","Norway","Egypt","Honduras","Moldova","Australia","Armenia","Oman","Kenya",
         "Bosnia and Herzegovina","Bahrain","Singapore","Latvia","Qatar","Zambia","Finland","Nigeria","Estonia","North Macedonia",
         "Algeria","Botswana","Zimbabwe","Albania","Uzbekistan","Kyrgyzstan","Mozambique","Montenegro","Afghanistan","Cyprus","Namibia","Ghana",
         "Uganda","El Salvador","Cambodia","Laos","Cameroon","Rwanda","Luxembourg","Maldives","Jamaica","Trinidad and Tobago",
         "Angola","Runion","Senegal","DRC","Malawi","Ivory Coast","Eswatini","Guadeloupe","Fiji","Suriname","Malta","Madagascar","Syria","Martinique",
         "French Guiana","Sudan","French Polynesia","Mauritania","Cabo Verde","Gabon","Guyana","Papua New Guinea","Belize","Guinea","Togo","Tanzania","Lesotho",
         "Barbados","Burundi","Iceland","Channel Islands","Haiti","Benin","Seychelles","Bahamas","Somalia","Mauritius","Andorra","Mayotte","Mali",
         "Curaao","Congo","Timor-Leste","Aruba","Burkina Faso","Nicaragua","Tajikistan","Taiwan","Brunei","South Sudan","New Zealand","Equatorial Guinea",
         "Djibouti","Isle of Man","Saint Lucia","New Caledonia","Hong Kong","CAR","Gambia","Yemen","Gibraltar","Cayman Islands",
         "Eritrea","San Marino","Niger","Sierra Leone","Dominica","Guinea-Bissau","Comoros","Liberia","Grenada","Liechtenstein","Bermuda",
         "St. Vincent Grenadines","Chad","Faeroe Islands","Sint Maarten","Monaco","Antigua and Barbuda","Saint Martin","Sao Tome and Principe",
         "Caribbean Netherlands","Turks and Caicos","British Virgin Islands","Saint Kitts and Nevis","Bhutan","Greenland","Anguilla",
         "St. Barth","Diamond Princess","Wallis and Futuna","Saint Pierre Miquelon","Falkland Islands","Macao","Montserrat","Vatican City","Solomon Islands",
         "Western Sahara","Palau","MS Zaandam","Vanuatu","Marshall Islands","Samoa","Saint Helena","Micronesia","Tonga","China"]

class GUILogin(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.geometry("500x250")
        self.title("TRA CỨU COVID-19")
        self.protocol("WM_DELETE_WINDOW", self.quitClose)
        self.resizable(0,0)

        box = tk.Frame(self)
        box.pack(side = "top", fill = "both", expand = True)
        
        box.grid_columnconfigure(0, weight = 1)
        box.grid_rowconfigure(0, weight = 1)

        # Chuyển đổi giữa các frame
        self.frames = {}
        for F in (LoginWindow, WorkingWindow):
            frame = F(box, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky= "nsew")

        self.nowSlide(LoginWindow)

    # Thay đổi kích thước frame
    def nowSlide(self, box):
        frame = self.frames[box]
        if box == WorkingWindow:
            self.geometry("900x600")
        else:
            self.geometry("600x380")
        frame.tkraise()

    def quitClose(self):
        if messagebox.askyesno("THOÁT CHƯƠNG TRÌNH", "BẠN CÓ MUỐN THOÁT KHÔNG?"):
            try:
                choice = EXIT
                client.sendall(choice.encode('utf-8'))
                client.close()
            except: 
                window = tkinter.Tk()
                window.wm_withdraw()
                window.geometry("1x1+200+200")
                messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
                client.close()
                sys.exit(0)

            self.destroy()

    def LoginIn(self, nowFrame, client):
        try:
            UserName = nowFrame.boxUser.get()
            Password = nowFrame.boxPassword.get()

            if Password == "":
                nowFrame.Notice["text"] = "Mật khẩu không thể để trống!"
                return
            elif UserName == "":
                nowFrame.Notice["text"] = "Tài khoản không thể để trống!"
                return
            elif UserName == "" and Password == "":
                nowFrame.Notice["text"] = "Tài khoản và mật khẩu trống"
                return

            #Client muốn LOGIN
            choice = LOGIN
            client.sendall(choice.encode('utf-8'))
            
            # Gửi tên đăng nhập cho Server
            client.sendall(UserName.encode('utf-8'))
            client.recv(1024)

            # Gửi mật khẩu cho Server
            client.sendall(Password.encode('utf-8'))
            client.recv(1024)

            check = client.recv(1024).decode('utf-8')
            if check == '1':
                self.nowSlide(WorkingWindow)
            elif check == '2':
                nowFrame.Notice["text"] = "Mật khẩu,tài khoản có thể sai hoặc chưa đăng ký"
            elif check == '0':
                nowFrame.Notice["text"] = "Bạn đã đăng nhập sẵn rồi!"

        except: 
            nowFrame.Notice["text"] = "Server không thể phản hồi!"
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
            client.close()
            sys.exit(0)

    def SignUp(self, nowFrame, client):
        try:
            UserName = nowFrame.boxUser.get()
            Password = nowFrame.boxPassword.get()

            if Password == "":
                nowFrame.Notice["text"] = "Mật khẩu không thể để trống!"
                return
            elif UserName == "":
                nowFrame.Notice["text"] = "Tài khoản không thể để trống!"
                return
            elif UserName == "" and Password == "":
                nowFrame.Notice["text"] = "Tài khoản và mật khẩu trống"
                return
            # Client muốn đăng ký
            choice = SIGNUP
            client.sendall(choice.encode('utf-8'))

            # Gửi tên đăng nhập cho Server
            client.sendall(UserName.encode('utf-8'))
            client.recv(1024)

            # Gửi mật khẩu cho Server
            client.sendall(Password.encode('utf-8'))
            client.recv(1024)
            
            check = client.recv(1024).decode('utf-8')
            if check == "True":
                messagebox.showwarning('Đăng ký', 'Đăng ký thành công')
                self.nowSlide(WorkingWindow)
            elif check == "Already":
                nowFrame.Notice["text"] = "Tài khoản đã đăng ký và có người sử dụng"
            elif check == "False":
                nowFrame.Notice["text"] = "Tài khoản đã tồn tại!!!"
            
        except:
            nowFrame.Notice["text"] = "Server không phản hồi, ngắt kết nối"
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
            client.close()
            sys.exit(0)

    def LogOut(self, nowFrame, client):
        try:
            # CLient muốn đăng xuất
            choice = LOGOUT
            client.sendall(choice.encode('utf-8'))

            check = client.recv(1024).decode('utf-8')
            if check == "True":
                self.nowSlide(LoginWindow)
                for i in nowFrame.tree.get_children():
                    nowFrame.tree.delete(i)
                nowFrame.update()
                client.sendall("Thoát tài khoản thành công!".encode('utf-8'))
        except:
            nowFrame.Notice["text"] = "Server Không phản hồi"
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
            client.close()
            sys.exit(0)

class LoginWindow(tk.Frame):

    def __init__(self, home, control):
        tk.Frame.__init__(self, home)
        self.configure(bg="#446980")

        tk.Label(self, text="TRA CỨU COVID-19", font=('LeagueGothic', 40, 'bold', 'italic', 'underline'), fg='#F5EB22',
                         bg='#446980').place(x=50, y=10)
        tk.Label(self, text='Tên đăng nhập ', font='40', bg='#446980', fg='white').place(x=75, y=150)
        tk.Label(self, text='Mật khẩu ', font='40', bg='#446980', fg='white').place(x=95, y=200)

        self.Notice = tk.Label(self, text="", bg="#446980", fg='red')

        self.boxUser = tk.Entry(self, width=35, bg='#dff0ee')
        self.boxPassword = tk.Entry(self, width=35, bg='#dff0ee',show='*')

        ButtLogin = tk.Button(self, text="Đăng nhập",bg="#0177d7", fg='#dff0ee',command=lambda: control.LoginIn(self, client))
        ButtLogin.configure(width=20,height=2)
        ButtSignup = tk.Button(self, text="Đăng ký", bg="#555555", fg='#dff0ee', command=lambda: control.SignUp(self, client))
        ButtSignup.configure(width=20,height=2)

        self.boxUser.place(x=185, y=150, width=300, height=25)
        self.boxPassword.place(x=185, y=200, width=300, height=25)
        self.Notice.place(x=240,y=330)

        ButtLogin.place(x=150, y=270)
        ButtSignup.place(x=300, y=270)

class WorkingWindow(tk.Frame):

    def __init__(self, home, control):
        tk.Frame.__init__(self, home)

        self.configure(bg="#66FFD6")

        top_frame = Frame(self, width=398, height=190, bg='#FFCCFF')
        top_frame.place(x=250, y=10)

        bot_frame = Frame(self, width=890, height=284, bg='#024b3f')
        bot_frame.place(x=5, y=250)


        TitleLabel2 = Label(top_frame, text="TRA CỨU THÔNG TIN COVID - 19",
                            font=('timenewroman', 19, 'bold', 'italic', 'underline'), bg="white", fg="#5A105A")
        TitleLabel2.place(x=0, y=0)

        TitleLabel = Label(self, text="BẢNG TRA CỨU THÔNG TIN COVID-19 TRÊN CÁC NƯỚC TRÊN THẾ GIỚI",
                           font=('timenewroman', 18, 'bold'), bg="#66FFD6", fg="#5A105A")
        TitleLabel.place(x=30, y=210)

        self.Notice = tk.Label(top_frame, text = "", bg = "#FFCCFF")
        self.Notice.place(x=130,y=170)

        self.tree = ttk.Treeview(bot_frame)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background = "white", foreground = "black", rowheight = 25, fieldbackground = "white")
        style.map("Treeview", background = [('selected', 'blue')])

        self.tree["column"] = ("Tên nước", "Số ca hôm nay", "Ca nhiễm", "Tử vong", "Hồi phục", "Nguy kịch", "Đang nhiễm")
        self.tree.column('#0', width = 0, stretch = tk.NO)
        self.tree.column("Tên nước", anchor = 'c', width = 120)
        self.tree.column("Số ca hôm nay", anchor = 'c', width = 120)
        self.tree.column("Ca nhiễm", anchor = 'c', width = 150)
        self.tree.column("Tử vong", anchor = 'c', width = 120)
        self.tree.column("Hồi phục", anchor = 'c', width = 120)
        self.tree.column("Nguy kịch", anchor = 'c', width = 120)
        self.tree.column("Đang nhiễm", anchor = 'c', width = 120)

        self.tree.heading("0", text = "", anchor = 'c')
        self.tree.heading("Tên nước", text = "TÊN NƯỚC", anchor = 'c')
        self.tree.heading("Số ca hôm nay", text = "CA HÔM NAY", anchor = 'c')
        self.tree.heading("Ca nhiễm", text = "TỔNG CA NHIỄM", anchor = 'c')
        self.tree.heading("Tử vong", text = "TỬ VONG", anchor = 'c')
        self.tree.heading("Hồi phục", text = "HỒI PHỤC", anchor = 'c')
        self.tree.heading("Nguy kịch", text = "NGUY KỊCH", anchor = 'c')
        self.tree.heading("Đang nhiễm", text = "ĐANG NHIỄM" , anchor = 'c')
        self.tree.place(x=9,y=8)

        self.EntrySearch = Combobox(top_frame,width=35,font='Calibri 15',background='#FFE4E4',values=COUNTRY)
        self.EntrySearch.place(x=20, y=83)

        self.LabelEntry = tk.Label(top_frame, text="NHẬP TÊN QUỐC GIA CẦN TRA CỨU", font=('timenewroman', 15, 'bold'),
                                   bg='#FFCCFF', fg="#5A105A")
        self.LabelEntry.place(x=20, y=50)
        self.table = self.tree


        Button(top_frame, text="TÌM KIẾM", command=self.searchBox, width=15, height=2).place(x=50, y=125)
        Button(top_frame, text="XÓA LIST", command=self.clearRow, width=15, height=2).place(x=230, y=125)
        Button(self,text="ĐĂNG XUẤT",command = lambda: control.LogOut(self, client), width = 15,height=2,fg="red").place(x=765,y=545)

        Label(text='"Tự bảo vệ chính bản thân mình và những người xung quanh để ngăn ngừa sự lây lan của COVID-19"',bg='#66FFD6',font=('DancingScript',12,"italic")).place(x=30,y=550)

    def searchBox(self):
        try:
            countryName = self.EntrySearch.get()
            if (countryName == ""):
                self.Notice["text"] = "Không được bỏ trống"
                return

            choice = SEARCH
            client.sendall(choice.encode('utf-8'))

            boxForData = []
            self.Notice["text"] = ""

            client.sendall(countryName.encode('utf-8'))
            client.recv(1024).decode('utf-8')

            checkIsTrue = client.recv(1024).decode('utf-8')
            if (checkIsTrue == "-1"):
                self.Notice["text"] = "Nhập dữ liệu sai, vui lòng nhập lại!"
                return

            boxForData.append(countryName)

            client.sendall("Client gửi lại phản hồi".encode('utf-8'))
            todaycase = client.recv(1024).decode('utf-8')
            boxForData.append(todaycase)

            client.sendall("Client gửi lại phản hồi".encode('utf-8'))
            cases = client.recv(1024).decode('utf-8')
            boxForData.append(cases)

            client.sendall("Client gửi lại phản hồi ".encode('utf-8'))
            deaths = client.recv(1024).decode('utf-8')
            boxForData.append(deaths)

            client.sendall("Client gửi lại phản hồi ".encode('utf-8'))
            recovered = client.recv(1024).decode('utf-8')
            boxForData.append(recovered)

            client.sendall("Client gửi lại phản hồi".encode('utf-8'))
            critical = client.recv(1024).decode('utf-8')
            boxForData.append(critical)

            client.sendall("Client gửi lại phản hồi".encode('utf-8'))
            active = client.recv(1024).decode('utf-8')
            boxForData.append(active)

            self.tree.tag_configure('odd', background = 'white')
            self.tree.tag_configure('even', background = '#CCCCFF')

            global idx
            if idx % 2 == 0:
                self.table.insert(parent = "", index = "end", iid = idx, values = (boxForData[0], boxForData[1], boxForData[2], boxForData[3], boxForData[4], boxForData[5], boxForData[6]), tags = ('even',))
            else:
                self.table.insert(parent = "", index = "end", iid = idx, values = (boxForData[0], boxForData[1], boxForData[2], boxForData[3], boxForData[4], boxForData[5], boxForData[6]), tags = ('odd',))
            idx += 1

        except:
            self.Notice["text"] = "Server không phản hồi, ngắt kết nối!"
            window = tkinter.Tk()
            window.wm_withdraw()
            window.geometry("1x1+200+200")
            messagebox.showwarning('SERVER KHÔNG PHẢN HỒI','SERVER ĐÃ NGẮT KẾT NỐI')
            client.close()
            sys.exit(0)

    def clearRow(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.update()
# Kết nối
def Connect():
    global client
    try:
        # Tạo kết nối
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        sys.exit(1)
    try:
        HOST = Host.get()
        PORT = Port.get()
        serverAdrr = HOST, int(PORT)
        # Client gởi yêu cầu nối kết đến server có địa chỉ IP và Port xác định
        client.connect(serverAdrr)
        messagebox.showinfo("Kết nối", "Kết nối thành công  !!!")
    except:
        messagebox.showinfo("Kết nối", "IP, Port sai hoặc không tìm thấy Server, vui lòng kiểm tra lại !!!")
        return
    try:
        Client.destroy()
        app = GUILogin()
        app.mainloop()
    except:
        client.close()
        sys.exit(1)
    finally:
        client.close()

if __name__ == '__main__':

    Client = tk.Tk()
    Client.geometry('400x150')
    Client.title('Kết nối')
    Client.resizable(0, 0)
    Client.configure(bg='#202123')

    Host = Entry(Client, width=60)
    HostLabel = Label(Client, text='Nhập địa chỉ IP Server:', bg='#202123', fg='white')
    HostLabel.place(x=10, y=10)
    Host.place(x=10, y=35, width=300, height=25)

    Port = Entry(Client, width=60)
    PortLabel = Label(Client, text='Nhập số Port (65489):', bg='#202123', fg='white')
    PortLabel.place(x=10, y=70)
    Port.place(x=10, y=95, width=300, height=25)

    ConnectBtn = Button(Client, text='Kết nối', width=7, height=5, bg='#3A71B1', fg='white',
                        command=lambda: Connect())
    ConnectBtn.place(x=325, y=37)

    Client.mainloop()



