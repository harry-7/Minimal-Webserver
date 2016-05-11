import socket

port = input("PORT: ")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "0.0.0.0"
try:
    s.bind((host, port))
except:
    print "Socket creation Error"
    exit(0)
s.listen(15)
print "Server is Up and Running on ", port

while True:
    try:
        cs, addr = s.accept()
        try:
            request = cs.recv(1024)
            inp = request.split()
            if inp[0] == 'GET':
                filename = inp[1]
                # print filename,"First one"
                if filename[len(filename) - 1] == '/':
                    filename += "index.html"
                filename = filename[1:]

                try:
                    fp = open(filename, 'rb')
                    op = fp.read()
                    cs.send('\nHTTP/1.1 200 OK\n\n')
                    cs.send(op)
                    cs.close()
                except IOError:
                    """ Sending a 404 Not Found file"""
                    cs.send('\nHTTP/1.1 200 OK\n\n')
                    message = '<!DOCTYPE html>\n<html lang="en">\n\t<head>\n\t\t<title>404 Page Not Found</title>\n\t\t' \
                              '<style type="text/css">' \
                              '\n\t\t\t::selection{background-color: #2094CF;color: white; }\n\t\t\t::moz-selection{background-color: #2094CF;color: white; }\n\t\t\t::webkit-selection{background-color: #2094CF;color: white; }\n\t\t\t' \
                              'body{background-color:#f2f2f2;margin:40px;font-family:\'Open sans\',sans-serif}\n\t\t\t#container{margin:auto;text-align:center}\n\t\t\th1{font-size:72px}\n\t\t\th1,h2{font-weight:400}\n\t\t\th2{color:#aaa}\n\t\t\ta{color:#08c;text-decoration:none}\n\t\t' \
                              '</style>\n\t' \
                              '</head>\n\t' \
                              '<body>\n\t\t<div id="container">\n\t\t\t<h1>404</h1>\n\t\t\t<h2>Page not found!</h2>\n\t\t\t' \
                              '<h2>Sorry, the page you were looking for was not found.</h2>\n\t\t' \
                              '</div>\n\t</body>\n</html>\n\n'
                    cs.send(message)
                    cs.close()
        except:
            cs.close()
            print "Connection closed"
    except:
        print "\nBye"
        s.close()
        exit(0)
s.close()
