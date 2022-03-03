from musocapp import __app_name__
from musocapp.cli import app

def main():
    return app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
