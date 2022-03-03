from musoapp import __app_name__
from musoapp.cli import app

def main():
    return app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
