import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QListWidget
from ftplib import FTP

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Online Storage")
        self.resize(400, 300)

        self.login_widget = LoginWidget(self)
        self.setCentralWidget(self.login_widget)

        self.ftp = FTP('ftpupload.net')  # Replace with your FTP server details

    def handle_login(self, username, password):
        try:
            self.ftp.login(username, password)
            self.file_widget = FileWidget(self)
            self.setCentralWidget(self.file_widget)
            self.file_widget.list_files()
        except Exception as e:
            print("Login Error:", str(e))

    def handle_upload(self):
        file_dialog = QFileDialog()
        file_path = file_dialog.getOpenFileName(self, "Select File to Upload")
        if file_path[0]:
            file_name = file_path[0].split("/")[-1]
            with open(file_path[0], 'rb') as file:
                try:
                    self.ftp.storbinary(f"STOR {file_name}", file)
                    self.file_widget.list_files()
                except Exception as e:
                    print("Upload Error:", str(e))

    def handle_download(self):
        selected_item = self.file_widget.file_list.currentItem()
        if selected_item is not None:
            file_name = selected_item.text()
            with open(file_name, 'wb') as file:
                try:
                    self.ftp.retrbinary(f"RETR {file_name}", file.write)
                except Exception as e:
                    print("Download Error:", str(e))

    def handle_exit(self):
        self.ftp.quit()
        self.close()


class LoginWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.parent().handle_login(username, password)


class FileWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.file_list = QListWidget()
        layout.addWidget(self.file_list)

        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.parent().handle_upload)
        layout.addWidget(self.upload_button)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.parent().handle_download)
        layout.addWidget(self.download_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.parent().handle_exit)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def list_files(self):
        self.file_list.clear()
        files = self.parent().ftp.nlst()
        self.file_list.addItems(files)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
