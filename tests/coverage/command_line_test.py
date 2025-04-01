from os import system


def test_command_line():
    system("python gherkin_processor/main.py -h")
