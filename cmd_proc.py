def command_processor(command_handler):
    while True:
        cmd = raw_input()

        if not cmd:
            continue

        if cmd[0] == ' ':
            cmd = cmd[1:]

        if cmd.count(' '):
            raw = cmd[cmd.find(' ') + 1:]
            args = raw.split(' ')
            cmd = cmd[:cmd.find(' ')]
        else:
            raw = args = None

        try:
            getattr(command_handler, cmd)(args, raw)
            # eval('CommandHandler().{0}({1}, "{2}")'.format(cmd, args, raw))
        except AttributeError:
            print 'Unknown command: {0}'.format(cmd)

