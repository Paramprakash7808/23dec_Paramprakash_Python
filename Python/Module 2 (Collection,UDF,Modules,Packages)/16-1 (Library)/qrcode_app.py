import qrcode

url = 'https://solvera.pythonanywhere.com'

qr = qrcode.make(url)
qr.save('Solvera.png')