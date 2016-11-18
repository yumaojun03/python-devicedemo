from devicedemoclient.v1.api import client as v1_client


def client(version='1', **kwargs):
    """
    Factory function to create a new devicedemo service client.

    :param version <str> the client version
    :return Client
    """
    if version != '1':
        raise ValueError(
            "devicedemo only has one API version. Valid values for 'version'"
            " are '1'"
        )
    return v1_client.Client(**kwargs)
