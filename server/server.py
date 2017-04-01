import json
import command
import connection
import client_factory as client


# noinspection PyClassHasNoInit
class Command:
    @staticmethod
    def test(args, raw):
        print("[debug] actual test @ server")
        print args
        print raw

    @staticmethod
    def msg(args, raw):
        print "[debug] sending: " + raw
        client.message_all(raw)

    @staticmethod
    def cmd(args, raw):
        [cmd, args, raw] = command.normalize(raw)
        print "[debug] sending: {0}, {1}, {2}".format(cmd, args, raw)
        client.message_all(json.dumps({'command': cmd, 'args': args, 'raw': raw}))


def main():
    connection.init(client, 'localhost', 9999)  # todo read config
    command.processor(Command)

if __name__ == '__main__':
    main()
