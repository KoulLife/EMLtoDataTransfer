from tnefparse.tnef import TNEF
from tnefparse.utils import encode_tnef

# PDF 파일을 바이너리로 읽기
pdf_file_path = "example.pdf"
with open(pdf_file_path, "rb") as f:
    pdf_data = f.read()

# TNEF 첨부 파일 구조 생성
tnef_attachments = [{
    'data': pdf_data,
    'filename': 'example.pdf',
    'mimetype': 'application/pdf',
    'encoding': 'binary',
}]

# TNEF 메타데이터 설정
tnef_metadata = {
    'subject': 'Example Subject',
    'message_class': 'IPM.Note',
    'attachments': tnef_attachments,
}

# TNEF 파일로 인코딩
tnef_data = encode_tnef(tnef_metadata)

# TNEF 파일로 저장
tnef_file_path = "output.dat"
with open(tnef_file_path, "wb") as f:
    f.write(tnef_data)
