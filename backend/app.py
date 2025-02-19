import os
from __init__ import create_app
app = create_app()

if __name__ == '__main__':
    app.run(host='localhost', port=2025,debug=True)