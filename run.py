from app import WebApp

if __name__ == '__main__':
    server = WebApp('0.0.0.0', 8080, os.getenv('DATABASE_CONNECTION'))
    server.run_server()