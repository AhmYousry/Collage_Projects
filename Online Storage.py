import tkinter as tk
import tkinter.filedialog
import ftplib
import shutil



class FTPClientGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Create GUI elements
        self.hostname_label = tk.Label(self, text="Hostname:")
        self.hostname_entry = tk.Entry(self)
        self.username_label = tk.Label(self, text="Username:")
        self.username_entry = tk.Entry(self)
        self.password_label = tk.Label(self, text="Password:")
        self.password_entry = tk.Entry(self, show="*")
        self.connect_button = tk.Button(self, text="Connect", command=self.connect)
        self.button_logout = tk.Button(self, text="Disconnect", command=self.logout, state=tk.DISABLED)
        self.button_download = tk.Button(self, text="Download", command=self.download, state=tk.DISABLED)
        self.button_upload = tk.Button(self, text="Upload", command=self.upload, state=tk.DISABLED)
        self.output_text = tk.Text(self)

        # Layout GUI elements
        self.hostname_label.grid(row=0, column=0, sticky="e")
        self.hostname_entry.grid(row=0, column=1)
        self.username_label.grid(row=1, column=0, sticky="e")
        self.username_entry.grid(row=1, column=1)
        self.password_label.grid(row=2, column=0, sticky="e")
        self.password_entry.grid(row=2, column=1)
        self.connect_button.grid(row=3, column=0)
        self.button_logout.grid(row=3, column=1)
        self.button_download.grid(row=4, column=0)
        self.button_upload.grid(row=4, column=1)
        self.output_text.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def connect(self):
        # Get the hostname, username, and password from the GUI
        hostname = self.hostname_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Connect to the FTP server
        self.ftp = ftplib.FTP()
        self.ftp.connect('Local_Server', 21)
        self.ftp.login(username, password)

        # Get a list of files in the current directory and display them in the output text area
        files_list = self.ftp.nlst()
        files = self.ftp.retrlines("LIST")
        self.output_text.insert("end",hostname + ' is Connected... \n')
        for i in range(len(files_list)):
            file = files_list[i] + '\n'
            self.output_text.insert("end", file)

        self.connect_button.config(state=tk.DISABLED)
        self.button_logout.config(state=tk.NORMAL)
        self.button_download.config(state=tk.NORMAL)
        self.button_upload.config(state=tk.NORMAL)

    
    def logout(self):
        # Disconnect from FTP server
        self.ftp.quit()
            
        # Update GUI
        self.connect_button.config(state=tk.NORMAL)
        self.button_logout.config(state=tk.DISABLED)
        self.button_download.config(state=tk.DISABLED)
        self.button_upload.config(state=tk.DISABLED)
        self.output_text.insert("end", "Disconnected... \n")


    def download(self):
        # Prompt user for file to download
        file_to_download = tk.filedialog.askopenfilename(title="Select file to download")
        file_to_download = str(file_to_download)
        # Download file
        shutil.copy(file_to_download, 'local_file')
        self.output_text.insert("end",'Download Done... \n')
        


    def upload(self):
        # Prompt user for file to upload
        file_to_upload = tk.filedialog.askopenfilename(title="Select file to upload")
        file_to_upload = str(file_to_upload)
        # Upload file
        shutil.copy(file_to_upload, self.username_entry.get())
        self.output_text.insert("end",'Upload Done... \n')

    

if __name__ == "__main__":
    root = tk.Tk()
    root.title("FTP Client")
    FTPClientGUI(root).pack(fill="both", expand=True)
    root.mainloop()

