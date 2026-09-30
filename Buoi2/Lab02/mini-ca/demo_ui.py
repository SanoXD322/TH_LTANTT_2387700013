import os
import tkinter as tk
from tkinter import messagebox
from ca_utils import create_root_ca, create_intermediate_ca, issue_certificate, verify_certificate_chain, load_cert
from revoke_utils import revoke_certificate, check_revocation_status
from cryptography import x509

root_key, root_cert, inter_key, inter_cert = None, None, None, None

class CADemoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mini CA Demo UI")
        self.geometry("450x350")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Mini CA Demo", font=("Arial", 16, "bold")).pack(pady=10)
        self.log_text = tk.Text(self, height=10, width=55, state='disabled', bg="#f0f0f0")
        self.log_text.pack(pady=10)
        
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="1. Tạo Root & Intermediate CA", command=self.setup_ca).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="2. Phát hành User Cert", command=self.issue_cert).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="3. Kiểm tra Chuỗi Cert", command=self.verify_chain).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="4. Thu hồi User Cert", command=self.revoke_cert).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="5. Kiểm tra Trạng thái OCSP", command=self.ocsp_check).grid(row=2, column=0, columnspan=2, pady=5)

    def log(self, msg):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')

    def setup_ca(self):
        global root_key, root_cert, inter_key, inter_cert
        self.log("Tạo Root CA...")
        root_key, root_cert = create_root_ca()
        self.log("Tạo Intermediate CA...")
        inter_key, inter_cert = create_intermediate_ca(root_key, root_cert)
        messagebox.showinfo("Thông báo", "Đã tạo Root và Intermediate CA thành công!")

    def issue_cert(self):
        global inter_key, inter_cert
        if not inter_key:
            messagebox.showerror("Lỗi", "Phải tạo CA trước!")
            return
        subject_info = {"common_name": "Phuoc_Nguyen", "org": "PHUOCNTMH Company", "country": "VN"}
        self.log("Phát hành chứng chỉ người dùng cuối...")
        issue_certificate(inter_key, inter_cert, subject_info)
        messagebox.showinfo("Thông báo", "Phát hành chứng chỉ thành công!")

    def verify_chain(self):
        cert_path = os.path.join("certs", "Phuoc_Nguyen_cert.pem")
        if not os.path.exists(cert_path):
            messagebox.showerror("Lỗi", "Chưa có chứng chỉ user!")
            return
        chain_paths = [os.path.join("certs", "intermediate_cert.pem"), os.path.join("certs", "root_ca_cert.pem")]
        chain_certs = [load_cert(p) for p in chain_paths]
        valid = verify_certificate_chain(load_cert(cert_path), chain_certs)
        self.log(f"Chuỗi hợp lệ: {valid}")
        messagebox.showinfo("Kết quả", f"Chuỗi chứng chỉ hợp lệ: {valid}")

    def revoke_cert(self):
        cert_file = os.path.join("certs", "Phuoc_Nguyen_cert.pem")
        if not os.path.exists(cert_file):
            messagebox.showerror("Lỗi", "Thiếu file chứng chỉ để thu hồi!")
            return
        self.log("Thu hồi chứng chỉ user...")
        revoke_certificate(cert_file, os.path.join("certs", "intermediate_cert.pem"), os.path.join("certs", "intermediate_key.pem"))
        messagebox.showinfo("Thông báo", "Chứng chỉ đã được thu hồi!")

    def ocsp_check(self):
        cert_file = os.path.join("certs", "Phuoc_Nguyen_cert.pem")
        if not os.path.exists(cert_file):
            messagebox.showerror("Lỗi", "Chưa có chứng chỉ user!")
            return
        status = check_revocation_status(cert_file)
        self.log(f"Trạng thái OCSP: {'Đã thu hồi' if status else 'Hợp lệ'}")
        messagebox.showinfo("Kết quả OCSP", f"Trạng thái: {'Đã thu hồi' if status else 'Hợp lệ'}")

if __name__ == "__main__":
    app = CADemoApp()
    app.mainloop()
