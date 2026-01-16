import qrcode

url = 'https://github.com/Paramprakash7808/23dec_Paramprakash_Python'

qr = qrcode.make(url)
qr.save('Github.png')