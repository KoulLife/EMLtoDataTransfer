import os
from tnefparse.tnef import TNEF, TNEFAttachment, TNEFObject
from tnefparse.mapi import TNEFMAPI_Attribute

def unzip_dat(dat):
    print("unzip")
    # 지정된 폴더에 파일을 저장하기 위해 폴더를 생성
    output_directory = "./extracted_dat_files"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # dat이 파일 경로가 아니라 바이트 데이터일 경우 바로 처리
    if isinstance(dat, bytes):
        t = TNEF(dat, do_checksum=True)
    else:
        # dat이 경로인 경우 파일을 열고 바이트 데이터를 읽어 처리
        with open(dat, 'rb') as f:
            t = TNEF(f.read(), do_checksum=True)

    # 추출된 파일들의 경로를 저장할 리스트
    extracted_files = []

    # 각 첨부 파일을 지정된 폴더에 저장
    for a in t.attachments:
        output_path = os.path.join(output_directory, a.name)
        with open(output_path, "wb") as afp:
            afp.write(a.data)
        extracted_files.append(output_path)

    # 추출된 파일의 개수와 위치를 출력
    print("Successfully wrote %i files:" % len(t.attachments))
    for file in extracted_files:
        print(file)

    return extracted_files
