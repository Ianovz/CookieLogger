import pytest
from myApp.cookie_logger.main import CookieLogger
from pathlib import Path

@pytest.fixture
def file_path():
    return (Path(__file__).parents[1] / 'data' / 'cookies.csv').resolve()

def test_parse_log_file(file_path):
    cookie_logger = CookieLogger(str(file_path))
    cookie_logger.parse_log_file('2018-12-09')
    assert cookie_logger.cookie_counters == {'AtY0laUfhglK3lC7': 2, '5UAVanZf6UtGyKVS': 1, 'SAZuXPGUrfbcn5UA': 1}

def test_find_most_active_cookies(file_path):
    cookie_logger = CookieLogger(str(file_path))
    cookie_logger.cookie_counters = {'AtY0laUfhglK3lC7': 2, '5UAVanZf6UtGyKVS': 1, 'SAZuXPGUrfbcn5UA': 1}
    assert cookie_logger.find_most_active_cookies() == ['AtY0laUfhglK3lC7']

def test_file_not_found_exception(mocker):
    mocker.patch("builtins.open", side_effect=FileNotFoundError)
    with pytest.raises(FileNotFoundError):
        cookie_logger = CookieLogger('nonexistent_file.csv')
        cookie_logger.parse_log_file('2018-12-09')

def test_parse_log_file_success(mocker):
    mock_file_content = "cookie,timestamp\nAtY0laUfhglK3lC7,2018-12-09T14:19:00+00:00\n"
    mocker.patch("builtins.open", mocker.mock_open(read_data=mock_file_content))
    cookie_logger = CookieLogger('dummy_path.csv')
    cookie_logger.parse_log_file('2018-12-09')
    assert cookie_logger.cookie_counters['AtY0laUfhglK3lC7'] == 1

def test_parse_log_file_empty(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data=""))
    cookie_logger = CookieLogger('empty_file.csv')
    cookie_logger.parse_log_file('2018-12-09')
    assert cookie_logger.cookie_counters == {}
