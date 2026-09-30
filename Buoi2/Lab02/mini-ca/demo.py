import os
from cryptography import x509
from ca_utils import create_root_ca, create_intermediate_ca, issue_certificate, verify_certificate_chain, load_cert
from revoke_utils import revoke_certificate, check_revocation_status

root_key, root_cert, inter_key, inter_cert = None, None, None, None

def setup_ca():
    global root_key, root_cert, inter_key, inter_cert
    print("Tạo Root CA...")
    root_key, root_cert = create_root_ca()
    print("Tạo Intermediate CA...")
    inter_key, inter_cert = create_intermediate_ca(root_key, root_cert)

def issue_cert_demo():
    subject_info = {"common_name": "Phuoc_Nguyen", "org": "PHUOCNTMH Company", "country": "VN"}
    print("Phát hành chứng chỉ người dùng cuối...")
    cert_key, cert = issue_certificate(inter_key, inter_cert, subject_info)
    return os.path.join("certs", f"{subject_info['common_name']}_cert.pem")

def verify_chain_demo(user_cert_path):
    print("Kiểm tra chuỗi chứng chỉ...")
    chain_paths = [os.path.join("certs", "intermediate_cert.pem"), os.path.join("certs", "root_ca_cert.pem")]
    chain_certs = [load_cert(p) for p in chain_paths]
    user_cert = load_cert(user_cert_path)
    valid = verify_certificate_chain(user_cert, chain_certs)
    print(f"Chuỗi hợp lệ: {valid}")

def revoke_demo():
    print("Thu hồi chứng chỉ user...")
    revoke_certificate(
        os.path.join("certs", "Phuoc_Nguyen_cert.pem"),
        os.path.join("certs", "intermediate_cert.pem"),
        os.path.join("certs", "intermediate_key.pem")
    )
    print("Đã thu hồi")

def ocsp_check_demo():
    print("Kiểm tra trạng thái OCSP...")
    status = check_revocation_status(os.path.join("certs", "Phuoc_Nguyen_cert.pem"))
    print(f"Trạng thái: {'Revoked' if status else 'Valid'}")

if __name__ == "__main__":
    setup_ca()
    user_cert = issue_cert_demo()
    verify_chain_demo(user_cert)
    revoke_demo()
    ocsp_check_demo()
