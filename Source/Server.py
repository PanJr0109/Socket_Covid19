import tkinter as tk
import tkinter
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import *
import threading
import json
import socket
from urllib.request import urlopen
import sys

PORT = 65489

LOGIN = "login"
LOGOUT = "logout"
SIGNUP = "signup"
EXIT = "out"
FONT = ("timenewroman", 25, "bold")
SEARCH = "search"
member = 0

try:
    # Tạo kết nối (AF_INET là kiểu thiết lập kết nối IPv4, SOCK_STREAM là giao thức kết nối TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Địa chỉ IP của server (máy chủ)
    HOSTNAME = socket.gethostname()
    ADDRESS = socket.gethostbyname(HOSTNAME)
    # Lỗi kết nối khi tạo socket
except socket.error as er:
    sys.exit(1)

try:
    # Server yêu cầu gán số hiệu cổng (port) cho socket
    server.bind((ADDRESS, PORT))
    # Server lắng nghe các yêu cầu nối kết từ các client trên cổng đã được gán
    server.listen(5)
# Lỗi địa chỉ kết nối
except socket.gaierror as e:
    sys.exit(1)
# Lỗi kết nối
except socket.error as e:
    sys.exit(1)


# Hàm dùng để giao tiếp giữa Server và Client
def handleClient(Client_Sock, Client_Address):
    try:
        while True:
            choice = Client_Sock.recv(1024).decode('utf-8')
            if choice == LOGIN:
                SignIn_Client(Client_Sock, Client_Address)
            elif choice == SIGNUP:
                SignUp_Client(Client_Sock, Client_Address)
            elif choice == LOGOUT:
                SignOut_Client(Client_Sock, Client_Address)
            elif choice == EXIT:
                Exit_Client(Client_Address)
                break
            elif choice == SEARCH:
                SendData_Client(Client_Sock)
            else:
                break
        Client_Sock.close()
    # Trường hợp ngoại lệ
    except OSError:
        return
    finally:
        Client_Sock.close()


# Giao tiếp với nhiều client
def handleServer():
    try:
        while True:
            # Server chấp nhận nối kết của client, khi đó một kênh giao tiếp ảo được hình thành
            Client_Sock, Client_Address = server.accept()
            # Kết nối đa luồng
            threading.Thread(target=handleClient, daemon=True, args=(Client_Sock, Client_Address)).start()

    except KeyboardInterrupt:
        server.close()
    finally:
        server.close()


# Lấy dữ liệu COVID-19 và lưu vào file
def get_Data(filename):
    # truy cập link để lấy thông tin Covid
    url = "https://coronavirus-19-api.herokuapp.com/countries"
    response = urlopen(url)
    data = json.loads(response.read())

    json_object = json.dumps(data, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)


# Quản lý các thông tin "tên đăng nhập","Mật khẩu","Tình trạng đăng nhập" của các users
class manage_Account:

    def __init__(self, username, password):
        self.user = username
        self.password = password

    # Tạo tài khoản
    def createAccount(self):
        with open('Account.json', 'r+') as file:
            file_data = json.load(file)
            file_data["Account"].append(self.user)
            file_data["Password"].append(self.password)
            # Lưu thêm tên đăng nhập và mật khẩu vào file Account.json
            file.seek(0)
            json.dump(file_data, file, indent=4)

    # Kiểm tra tên đăng nhập đã được đăng ký hay chưa
    def checkSignUp(self):
        if self.checkOnlineAccount() == True:
            return "0"
        with open('Account.json') as file:
            file_data = json.load(file)
        if self.user in file_data["Account"]:
            return "1"
        else:
            return "2"

    # Kiểm tra thông tin khi đăng nhập
    def checkSignIn(self):
        with open('Account.json') as file:
            file_data = json.load(file)

        if self.checkOnlineAccount() == True:
            return "0"

        if self.user in file_data["Account"]:
            i = file_data["Account"].index(self.user)
            if self.password in file_data["Password"]:
                j = file_data["Password"].index(self.password)
                if i == j:
                    return "1"
                return "2"
            else:
                return "2"
        else:
            return "2"

    # Lưu các tài khoản đang hoạt động
    def saveOnlineAccount(self, addr):
        with open('OnlineAccount.json', 'r+') as file:
            file_data = json.load(file)
            file_data["Account"].append(self.user)
            file_data["Address"].append(addr)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    # Kiểm tra tài khoản có đang hoạt động hay không
    def checkOnlineAccount(self):
        with open('OnlineAccount.json') as file:
            file_data = json.load(file)

        if self.user in file_data["Account"]:
            return True
        else:
            return False


# Xóa tài khoản đang hoạt động khi client thoát
def removeOnlineAccount(addr):
    with open('OnlineAccount.json') as file:
        file_data = json.load(file)

    try:
        i = 0
        for element in file_data["Address"]:
            if str(addr) in element:
                file_data["Address"].remove(str(addr))
                break
            i = i + 1

        del file_data["Account"][i]
        with open('OnlineAccount.json', 'w') as data_file:
            json.dump(file_data, data_file, indent=4)
    except:
        return

def SignIn_Client(server, addr):
    # Server nhận tên đăng nhập người dùng, sau đó gửi thông báo lại cho Client
    UserName = server.recv(1024).decode('utf-8')
    server.sendall("Đã nhận".encode('utf-8'))

    # Server nhận password người dùng, sau đó gửi thông báo lại cho Client
    Password = server.recv(1024).decode('utf-8')
    server.sendall("Đã nhận".encode('utf-8'))
    # Biến kiểm tra tình trạng đăng nhập
    Check = manage_Account(UserName, Password).checkSignIn()

    # check=1 -> Đăng nhập thành công
    if Check == '1':
        manage_Account(UserName, Password).saveOnlineAccount(str(addr))
    # Gửi lại check cho CLient xử lí
    server.sendall(Check.encode('utf-8'))


def SignUp_Client(server, addr):
    # Server nhận tên đăng nhập người dùng, sau đó gửi thông báo lại cho Client
    UserName = server.recv(1024).decode('utf-8')
    server.sendall("Đã nhận".encode('utf-8'))
    # Server nhận mật khẩu người dùng, sau đó gửi thông báo lại cho Client
    Password = server.recv(1024).decode('utf-8')
    server.sendall("Đã nhận".encode('utf-8'))

    Account =manage_Account(UserName, Password)
    # Kiểm tra tình trạng tài khoản để đăng ký
    Check = Account.checkSignUp()

    if Check == "2":  # Tài khoản sẽ được đăng ký thành công
        Account.createAccount()
        Account.saveOnlineAccount(str(addr))
        server.sendall("True".encode('utf8'))
    elif Check == "0":  # Tài khoản đang hoạt động ở một máy chủ khác
        server.sendall("Already".encode('utf-8'))
    elif Check == "1":  # Tài khoản đã được đăng ký
        server.sendall("False".encode('utf-8'))


# Đăng xuất tài khoản
def SignOut_Client(server, addr):
    # xóa tên đăng nhập và mật khẩu đang hoạt động trong file "OnlineAccount.json"
    removeOnlineAccount(addr)
    try:
        server.sendall("True".encode('utf-8'))
        server.recv(1024).decode('utf-8')
    except:
        messagebox.showwarning("Lỗi", "Lỗi mật khẩu hoặc tài khoản !!!")

# Thoát Client
def Exit_Client(addr):
    removeOnlineAccount(str(addr))
    window = tkinter.Tk()
    window.wm_withdraw()
    window.geometry("1x1+200+200")

# Quản lí dữ liệu COVID
class handleData:
    def __init__(self, name, filename):
        self.nameC = name
        self.file = filename

    def indexCountry(self):
        with open(self.file) as file:
            file_data = json.load(file)

        for i in range(len(file_data)):
            for key in file_data[i]:
                if file_data[i][key] == self.nameC:
                    return i
        return "-1"

    def cases(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["cases"]

    def todayCases(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["todayCases"]

    def deaths(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["deaths"]

    def todaydeaths(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["todayDeaths"]

    def recovered(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["recovered"]

    def active(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["active"]

    def critical(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["critical"]

    def casesPerOneMilion(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["casesPerOneMillion"]

    def deathsPerOneMillion(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["deathsPerOneMillion"]

    def totalTests(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["totalTests"]

    def testsPerOneMillion(self):
        idx = self.indexCountry()
        with open(self.file) as file:
            file_data = json.load(file)
        return file_data[idx]["testsPerOneMillion"]


def SendData_Client(server):
    try:
        countryBox = server.recv(1024).decode('utf-8')
        server.sendall("Nhận được phản hồi".encode('utf-8'))

        nameCountry = countryBox
        dataCovid = handleData(nameCountry, "data.json")
        checkName = dataCovid.indexCountry()

        server.sendall(str(checkName).encode('utf-8'))
        if (checkName == "-1"):
            return

        todayCases = dataCovid.todayCases()
        server.recv(1024).decode('utf-8')
        server.sendall(str(todayCases).encode('utf-8'))

        cases = dataCovid.cases()
        server.recv(1024).decode('utf-8')
        server.sendall(str(cases).encode('utf-8'))

        deaths = dataCovid.deaths()
        server.recv(1024).decode('utf-8')
        server.sendall(str(deaths).encode('utf-8'))

        recovered = dataCovid.recovered()
        server.recv(1024).decode('utf-8')
        server.sendall(str(recovered).encode('utf-8'))

        critical = dataCovid.critical()
        server.recv(1024).decode('utf-8')
        server.sendall(str(critical).encode('utf-8'))

        active = dataCovid.active()
        server.recv(1024).decode('utf-8')
        server.sendall(str(active).encode('utf-8'))

    except OSError:
        messagebox.showwarning("Lỗi", "LỖI LẤY DỮ LIỆU!!!")

# xóa tất cả account đang online khi tắt server
def OfflineALL():
    with open('OnlineAccount.json', 'r') as file:
        Acc = json.load(file)
        Acc['Account'].clear()
        Acc['Address'].clear()
    with open('OnlineAccount.json', 'w') as file:
        file.seek(0)
        json.dump(Acc, file, indent=4)


# Quản lí cửa số làm việc của Server
class GUISERVER(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        get_Data("data.json")

        self.title("SERVER")
        self.geometry("350x450")
        self.config(bg="#BBBBBB")
        self.protocol("WM_DELETE_WINDOW", self.quitServer)
        self.resizable(0, 0)
        Label(self, text="Đang hoạt động", bg="#BBBBBB", fg="#006600", width=20, font="timenewroman 12").place(x=85,
                                                                                                               y=10)

        Label(self, text="Số người đăng nhập hiện tại: " + str(member), bg="#BBBBBB", fg="#FF33CC").place(x=90, y=160)

        self.listBox = Listbox(self, height=10, width=37, bg="white", activestyle='dotbox', font='Calibri', fg="black")
        self.listBox.place(x=25, y=200)
        Button(self, text="Làm mới", bg="#3A71B1", fg='white', width=15, height=3, command=self.ClientUpdate).place(
            x=115, y=40)
        Button(self, text="Ngắt kết nối", bg="#3A71B1", fg='white', width=15, height=3, command=self.quitServer).place(
            x=115, y=100)

        self.refresh()
        self.mainloop()

    # Cập nhật số lượng Client truy cập
    def ClientUpdate(self):
        global member
        with open('OnlineAccount.json') as file:
            file_data = json.load(file)
        self.listBox.delete(0, len(file_data["Address"]))
        for i in range(len(file_data["Address"])):
            self.listBox.insert(i, "Đang truy cập: " + file_data["Address"][i])

        member = len(file_data["Address"])
        Label(self, text="Số người đăng nhập hiện tại: " + str(member), bg="#BBBBBB", fg="#FF33CC").place(x=90, y=160)

    # Thoát ứng dụng
    def quitServer(self):
        if messagebox.askokcancel("THOÁT CHƯƠNG TRÌNH?", "BẠN MUỐN THOÁT ỨNG DỤNG?"):
            OfflineALL()
            self.destroy()

    # Cập nhật thông tin 60 phút 1 lần
    def refresh(self):
        self.after(3600000, self.refresh)


if __name__ == '__main__':
    threading.Thread(target=handleServer, daemon=True).start()
    app = GUISERVER()
