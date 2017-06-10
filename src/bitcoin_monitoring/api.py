from logging import getLogger

from .utils import TwentyOneProviderRehive


logger = getLogger('django')


class AbstractBaseMonitoringInteface:
    """
    Template for Interface to handle all API calls to third-party account.
    """

    def get_transactions(self, address_list, limit=200, min_block=None) -> dict:
        """ Provides transactions associated with each address in address_list.
        Args:
            address_list (list): List of addresses.
            limit (int): Maximum number of transactions to return.
            min_block (int): Block height from which to start getting
                transactions. If None, will get transactions from the
                entire blockchain.
        Returns:
            dict: A dict keyed by address with each value being a list of
            Transaction objects.
        """
        raise NotImplementedError('subclasses of AbstractBaseUser must provide a get_transactions() method')


class BitcoinMonitoringInterface(AbstractBaseMonitoringInteface):
    """
    Interface implementation.
    """

    def __init__(self, *args, **kwargs):
        # Always linked to an AdminAccount
        super(BitcoinMonitoringInterface, self).__init__(*args, **kwargs)

        self.provider = TwentyOneProviderRehive()

    def get_transactions(self, address_list, limit=200, min_block=None):
        return self.provider.get_transactions_json(address_list=address_list, limit=limit, min_block=min_block)

    def get_transactions_by_id(self, ids):
        return self.provider.get_transactions_json_by_id(ids=ids)

    def get_block_height(self):
        return self.provider.get_block_height()


INTERFACES = {
    'bitcoin': BitcoinMonitoringInterface
}
