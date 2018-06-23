import socket
import sys

TEMPLATE_404 = 'templates/404.html'

if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.stderr.write('Usage: python server.py <port>\n')
        exit(-1)

    port = int(sys.argv[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '0.0.0.0'
    try:
        s.bind((host, port))
    except Exception as e:
        sys.stderr.write('Socket creation Error %s\n' % e)
        exit(-1)
    s.listen(15)
    sys.stderr.write('Server is Up and Running on %d\n' % port)

    while True:
        try:
            cs, addr = s.accept()
            try:
                request = cs.recv(1024)
                inp = request.split()
                sys.stderr.write(inp[0] + ' ')
                if inp[0] == 'GET':
                    filename = inp[1]
                    if filename[-1] == '/':
                        filename += 'index.html'
                    filename = filename[1:]
                    sys.stderr.write(filename + '\n')
                    try:
                        fp = open(filename, 'rb')
                        op = fp.read()
                        cs.send('\nHTTP/1.1 200 OK\n\n')
                        cs.send(op)
                    except Exception as e:
                        # Sending a 404 Not Found file
                        sys.stderr.write('Exception while reading file '
                                         + filename + ': ' + str(e) + '\n')
                        fp = open(TEMPLATE_404, 'rb')
                        op = fp.read()
                        cs.send('\nHTTP/1.1 404 NOT FOUND\n\n')
                        cs.send(op)
                    finally:
                        cs.close()
            except Exception as e:
                sys.stderr.write('Exception occured: ' + str(e))
                cs.close()
                print('Connection closed')
        except:
            sys.stderr.write('Shutting down Server\n')
            s.close()
            exit(0)
