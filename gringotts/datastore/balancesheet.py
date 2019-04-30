import attr

from gringotts.datastore import Account


class AccountNotFound(Exception):
    pass


@attr.s
class BalanceSheet:
    accounts = attr.ib(factory=dict)

    def get_account(self, name):
        account = self.accounts.get(name)
        if not account:
            raise AccountNotFound(str(name))
        return account

    def create_snapshot(self):
        snapshot = dict()

        for name, account in self.accounts.items():
            snapshot[name] = account.create_snapshot()

        return {'accounts': snapshot}

    @staticmethod
    def load_snapshot(snap):
        bs = BalanceSheet()
        for name, snap_acc in snap.accounts:
            bs.accounts[name] = Account.load_snapshot(snap_acc)

        return bs
