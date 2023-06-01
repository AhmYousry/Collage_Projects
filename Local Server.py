from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

# Create a dummy authorizer for managing users and permissions
authorizer = DummyAuthorizer()

# Allow anonymous users to read and write to the current working directory
authorizer.add_anonymous(".")
# Create an FTP handler that uses the dummy authorizer
handler = FTPHandler
handler.authorizer = authorizer
#Make a new directory for new user
if os.path.exists("local_file"):
    pass
else:
    os.mkdir("local_file")
#Username: admin , Password: admin
if os.path.exists('admin'):
    authorizer.add_user("admin", "admin", 'admin', perm="elradfmwMT")
else:
    # If the directory does not exist, create it
    os.mkdir('admin')
    authorizer.add_user("admin", "admin", 'admin', perm="elradfmwMT")
#Username: user1 , Password: user1
if os.path.exists('user1'):
    authorizer.add_user("user1", "user1", "user1", perm="elradfmwMT")
else:
    os.mkdir('user1')
    authorizer.add_user("user1", "user1", "user1", perm="elradfmwMT")
#Username: user2 , Password: user2
if os.path.exists('user2'):
    authorizer.add_user("user2", "user2", "user2", perm="elradfmwMT")
else:
    os.mkdir('user2')
    authorizer.add_user("user2", "user2", "user2", perm="elradfmwMT")

# Bind the FTP handler to a local address and port
server = FTPServer(("127.0.0.1", 21), handler)

# Start the FTP server
server.serve_forever()
