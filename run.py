from src.server import create_app

APP = create_app()

if __name__ == '__main__':
    APP.run(host="0.0.0.0")
