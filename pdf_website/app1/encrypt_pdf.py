#  add password to a pdf file

from PyPDF2 import PdfWriter, PdfReader

input_file = PdfReader('file1.pdf')
output_file = PdfWriter()
pwd ="#12345"
output_file.encrypt(pwd)

for i in range(len(input_file.pages)):
    data = input_file.pages[i]
    output_file.add_page(data)

with open("encrypted-file.pdf","wb") as file:
    output_file.write(file)

# print(input_file)