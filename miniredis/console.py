__metaclass__ = type
from cmd import Cmd

from redis_classes import RedisMessage, RedisError

INVALID_ARGS = "wrong number of arguments for '{}' command"


class Console(Cmd, object):

    def __init__(self, miniredis):
        Cmd.__init__(self)
        self.prompt = '> '
        self.lastcmd = False
        self.miniredis = miniredis
        self.command_list = [s[3:] for s in self.get_names() if s.startswith('do_')]
        self.command_list.sort()

    def exec_cmd(self, line):
        if not line:
            line = 'EOF'
        else:
            line = line.rstrip('\r\n')
        line = self.precmd(line)
        return self.onecmd(line)

    def parseline(self, line):
        cmd, arg, line = super(Console, self).parseline(line)
        return cmd.lower() if cmd else cmd, arg, line

    def default(self, line):
        self.stdout.write("(error) ERR unknown command '%s'\n" % line)
        self.stdout.write(" Valid commands (type 'help <command>' for info):  %s\n" % self.command_list)

    def emptyline(self):
        return None

    def postcmd(self, stop, line):
        """Hook method executed just after a command dispatch is finished."""
        if stop is None:
            return None
        elif isinstance(stop, RedisMessage):
            print(str(stop))
            return None
        elif isinstance(stop, str):
            print('"{}"'.format(stop))
            return None
        elif isinstance(stop, int):
            print('(integer) {}'.format(stop))
            return None
        elif isinstance(stop, list):
            for i, value in enumerate(stop):
                print('{}) "{}"'.format(i + 1, value))
            return None
        elif isinstance(stop, RedisError):
            print(str(stop))
            return None
        elif isinstance(stop, Exception):
            print(str(stop))
            return stop
        else:
            print(str(stop))
            return None

    def do_exit(self, line):
        """
            exit

        Stop the server.
        """
        print "Stopping MiniRedis console..."
        raise SystemExit

    def do_set(self, line):
        """
            SET key value [EX seconds]

        Set the string value of a key

        Optional:
            EX seconds -- Set the specified expire time, in seconds.
        """
        args = line.split()
        if len(args) == 2:
            return self.miniredis.set(args[0], args[1])
        elif len(args) == 3:
            return self.miniredis.set(args[0], args[1], args[2])
        else:
            return RedisError(INVALID_ARGS.format('SET'))

    def do_get(self, line):
        """
            GET key

        Get the value of a key
        """
        args = line.split()
        if len(args) == 1:
            return self.miniredis.get(args[0])
        else:
            return RedisError(INVALID_ARGS.format('GET'))

    def do_del(self, line):
        """
            DEL key

        Removes the specified keys. A key is ignored if it does not exist.
        """
        args = line.split()
        if len(args) == 1:
            return self.miniredis.delete(args[0])
        else:
            return RedisError(INVALID_ARGS.format('DEL'))

    def do_dbsize(self, line):
        """
            DBSIZE

        Return the number of keys in the selected database
        """
        args = line.split()
        if len(args) == 0:
            return self.miniredis.db_size()
        else:
            return RedisError(INVALID_ARGS.format('DBSIZE'))

    def do_incr(self, line):
        """
            INCR key

        Increment the integer value of a key by one
        """
        args = line.split()
        if len(args) == 1:
            return self.miniredis.incr(args[0])
        else:
            return RedisError(INVALID_ARGS.format('INCR'))

    def do_zadd(self, line):
        """
            ZADD key score member

        Add one member to a sorted set, or update its score if it already exists
        """
        args = line.split()
        if len(args) == 3:
            return self.miniredis.zadd(args[0], args[1], args[2])
        else:
            return RedisError(INVALID_ARGS.format('ZADD'))

    def do_zcard(self, line):
        """
            ZCARD key

        Get the number of members in a sorted set
        """
        args = line.split()
        if len(args) == 1:
            return self.miniredis.zcard(args[0])
        else:
            return RedisError(INVALID_ARGS.format('ZCARD'))

    def do_zrank(self, line):
        """
            ZRANK key member

        Determine the index of a member in a sorted set
        """
        args = line.split()
        if len(args) == 2:
            return self.miniredis.zrank(args[0], args[1])
        else:
            return RedisError(INVALID_ARGS.format('ZRANK'))

    def do_zrange(self, line):
        """
            ZRANGE key start stop

        Return a range of members in a sorted set, by index
        """
        args = line.split()
        if len(args) == 3:
            return self.miniredis.zrange(args[0], args[1], args[2])
        else:
            return RedisError(INVALID_ARGS.format('ZRANGE'))
