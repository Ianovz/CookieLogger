import subprocess
import pytest

@pytest.fixture
def cookie_log_file(tmp_path):
    data = """cookie,timestamp
AtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-09T10:13:00+00:00
5UAVanZf6UtGyKVS,2018-12-09T07:25:00+00:00
AtY0laUfhglK3lC7,2018-12-09T06:19:00+00:00
SAZuXPGUrfbcn5UA,2018-12-08T22:03:00+00:00
4sMM2LxV07bPJzwf,2018-12-08T21:30:00+00:00
fbcn5UAVanZf6UtG,2018-12-08T09:30:00+00:00
4sMM2LxV07bPJzwf,2018-12-07T23:30:00+00:00"""

    file = tmp_path / "cookie_log.csv"
    file.write_text(data)
    return file

def test_integration_cookie_finder(cookie_log_file):
    result = subprocess.run(['python3', 'myApp/cookie_logger/main.py', '-f', str(cookie_log_file), '-d', '2018-12-09'], capture_output=True, text=True)
    assert 'AtY0laUfhglK3lC7' in result.stdout