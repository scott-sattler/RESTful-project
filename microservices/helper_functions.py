"""

"""


def construct_address(host, port, route, args):
    """
        {host}:{port}{route}?{'&'.join(args)}

        :param str host: '172.0.0.1'
        :param str port: '5000'
        :param str route: '/store/file/here'
        :param list[str] args: ['a=b', 'c=d']
    """
    return f"http://{host}:{port}{route}?{'&'.join(args)}"


# host = '172.0.0.1'
# port = '5000'
# route = '/store'
# args = ['x=3', 'y=1']
# print(construct_address(host, port, route, args))
