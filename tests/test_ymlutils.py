import pytest
from utils.ymlutils import parse_yml, read_yml

@pytest.fixture(autouse=True)
def prepare_and_cleanup():
    # before
    print("before")
    yield
    # after
    print("after")

@pytest.mark.parametrize("param", ["test"])
def test_read_yml(param: str):
    # arrange
    mock_yml = """test:
    something: "xd"
    something2: 23
test2:
    - "one"
    - "two"
    - "three"
"""
    read_yml_mock = read_yml(mock_yml)
    with open("test.yml", "w") as file:
        file.write(mock_yml)

    # act
    read_yml_file = read_yml("test.yml")

    # assert
    assert read_yml_file == read_yml_mock