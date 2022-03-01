from muso import __version__, __app_name__


def test_version():
    assert __version__ == '0.1.0'
    
def test_name():
    assert __app_name__ == "Muso"
