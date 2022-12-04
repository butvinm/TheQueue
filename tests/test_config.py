from UeUBot.config import Config


def test_correct_env():
    config = Config('tests/testenvs/correct.env')
    assert config.TOKEN == '5155114149:AAEbaCdvL30kSRDC1vHavNlcO27EPvMY9iM'
    assert config.MESSAGES_STORAGE == './messages.json'
    assert config.QUEUES_STORAGE == './queues.json'


def test_losekey_env():
    config = Config('tests/testenvs/losekey.env')
    assert config.TOKEN == None
    assert config.MESSAGES_STORAGE == './messages.json'
    assert config.QUEUES_STORAGE == './queues.json'


def test_badfile_env():
    config = Config('tests/testenvs/badfile.env')
    assert config.TOKEN == None
    assert config.MESSAGES_STORAGE == None
    assert config.QUEUES_STORAGE == None
