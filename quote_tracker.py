from coinpaprika import client as Coinpaprika
from colorama import init, Fore, Back, Style

class Coin:
    def __init__(self, c_id=None, name=None, symbol=None, rank=None, price=None, del_hr=None, del_d=None, del_wk=None, del_m=None,
                 del_y=None):
        self.c_id = c_id
        self.c_name = name
        self.symbol = symbol
        self.rank = rank
        self.technical = {'p': price, 'd_h': del_hr, 'd_d': del_d, 'd_w': del_wk, 'd_m': del_m, 'd_y': del_y}

    def __repr__(self):
        s = ''
        for a in self.__dict__:
            s += f"{a}: {self.__getattribute__(a)}\n"
        return s


class PaprikaDAO:
    """
    Welcome to the crypto-quoter, Robert Silver 2021
    --Thank you to CoinPaprika API and to github user s0h3ck for their useful package
    ---https://api.coinpaprika.com/
    ---https://github.com/s0h3ck/coinpaprika-api-python-client


    """
    def __init__(self):
        self.client = Coinpaprika.Client()
        self.coin_dict = {}
        self.top = []

    def setup(self):
        self.init_coins_dict()
        self.get_top_10()

    def init_coins_dict(self):
        for c in self.client.coins():
            self.coin_dict[c['symbol']] = c['id']

    def get_top_10(self):
        self.top = [c['symbol'] for c in self.client.coins()[:10]]

    def retCoin(self, c_sym):
        if c_sym not in self.coin_dict:
            raise ValueError(f"Symbol {c_sym}: Not Recognized in API")
        c_id = self.coin_dict[c_sym]
        c_ret = self.client.coin(c_id)
        c_ticker =  self.client.ticker(c_id)
        c_tech = c_ticker['quotes']['USD']
        coin_ret = Coin(c_id,
                        c_ret['name'],
                        c_sym, c_ret['rank'],
                        c_tech['price'],
                        c_tech['percent_change_1h'],
                        c_tech['percent_change_24h'],
                        c_tech['percent_change_7d'],
                        c_tech['percent_change_30d'],
                        c_tech['percent_change_1y'])
        return coin_ret


if __name__ == "__main__":

    def check_exit(q):
        if q in ["exit", "e", "quit", "q"]:
            exit()

    def get_techs(c):
        for k, v in c.technical.items():
            if k != 'p':
                if v > 0:
                    c.technical[k] = Fore.GREEN + str(v)
                elif v < 0:
                    c.technical[k] = Fore.RED + str(v)
                else:
                    c.technical[k] = Fore.WHITE + str(v)

    def print_form(coins):
        print(f"{'NAME':30}|{'PRICE':15}|{'1h':^8}|{'24h':^8}|{'1w':^8}|{'1m':^8}|{'1y':^8}")
        print("-" * 95)

        for c in coins:
            get_techs(c)
            print(f"{c.c_name+' ('+c.symbol+')':30}|{'$' + str(round(c.technical['p'], 3)):>15}|{c.technical['d_h']:>12}%{Fore.RESET}|{c.technical['d_d']:>12}%{Fore.RESET}|{c.technical['d_w']:>12}%{Fore.RESET}|{c.technical['d_m']:>12}%{Fore.RESET}|{c.technical['d_y']:>12}%{Fore.RESET}")

    def disp_top(pDAO):
        top_coins = [pDAO.retCoin(sym) for sym in pDAO.top]
        print_form(top_coins)

    def disp_search(pDAO):
        msg = """
Enter the symbol of the coin you wish to search for, i.e. 'BTC' for Bitcoin, 'ETH' for Ethereum         
"""
        while True:
            c_choice = input(msg)
            try:
                coin_ret = pDAO.retCoin(c_choice)
                print_form([coin_ret])
                return
            except ValueError as e:
                msg = f"{e}" + "\nEnter the symbol of the coin you wish to search for, i.e. 'BTC' for Bitcoin, 'ETH' for Ethereum\n"

    def main():
        # for colorama
        init(autoreset=True)
        print(PaprikaDAO.__doc__)
        pDAO = PaprikaDAO()
        pDAO.setup()
        while True:
            msg = """
What would you like to see?
Type "top"/"t" for a ticker of the top 10 cryptos, or "search"/"s" to search by symbol
Type "exit"/"e" or "quit"/"q" to exit the program
"""
            type_query = input(msg)
            check_exit(type_query)
            if type_query in ["top", "t"]:
                disp_top(pDAO)
            elif type_query in ["search", "s"]:
                disp_search(pDAO)

    main()
