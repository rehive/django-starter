from datetime import datetime

from two1.blockchain import TwentyOneProvider
from collections import defaultdict


class TwentyOneProviderRehive(TwentyOneProvider):
    def get_transactions_json(self, address_list, limit=100, min_block=None):
        """ Provides transactions associated with each address in address_list.
        Args:
            address_list (list): List of Base58Check encoded Bitcoin
                addresses.
            limit (int): Maximum number of transactions to return.
            min_block (int): Block height from which to start getting
                transactions. If None, will get transactions from the
                entire blockchain.
        Returns:
            dict: A dict keyed by address with each value being a list of
            Transaction objects.
        """
        ret = defaultdict(list)
        for addresses in self._list_chunks(address_list, 199):
            path = "addresses/" + ",".join(addresses) \
                   + "/transactions?limit={}".format(limit)
            if min_block:
                path += "&min_block={}".format(min_block)

            r = self._request("GET", path)
            txn_data = r.json()

            for data in txn_data:
                txn, addr_keys = self.txn_from_json(data)
                for addr in addr_keys:
                    if addr in addresses:
                        ret[addr].append(data)

        return ret

    def get_transactions_json_by_id(self, ids):
        """ Gets transactions by their IDs.
        Args:
            ids (list): List of TXIDs to retrieve.
        Returns:
            dict: A dict keyed by TXID of Transaction objects.
        """
        ret = {}
        for txid in ids:
            response = self._request("GET", "transactions/%s" % txid)
            data = response.json()

            ret[txid] = data

        return ret



