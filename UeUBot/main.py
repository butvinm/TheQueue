from config import Config


def main():
    config = Config()
    print(config.TOKEN)
    print(config.QUEUES_STORAGE)
    print(config.MESSAGES_STORAGE)


if __name__ == '__main__':
    main()    
