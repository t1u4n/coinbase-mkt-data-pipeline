import websocket
import json
from threading import Thread
from typing import List

COINBASE_MKT_WEBSOCKET_API_PROD = 'wss://ws-feed.exchange.coinbase.com'
COINBASE_MKT_WEBSOCKET_API_SANDBOX = 'wss://ws-feed-public.sandbox.exchange.coinbase.com'



class CoinbaseDataIngestor:
    """This class is used to ingest data from Coinbase."""

    def __init__(self, url: str, channels: List[str], product_ids: List[str]):
        """Constructor of YFinanceDataIngestor."""
        self._url = url
        self.channels = channels
        self.product_ids = product_ids
        self._ws = websocket.WebSocketApp(self._url,
                                         on_open=self._on_open,
                                         on_message=self._on_message,
                                         on_error=self._on_error,
                                         on_close=self._on_close)
    
    def _on_message(self, ws: 'websocket.WebSocketApp', msg: str) -> None:
        """This method is used to handle the message received from Coinbase."""
        print(f'Msg: {msg}')
    
    def _on_error(self, ws: 'websocket.WebSocketApp', err: str) -> None:
        """This method is used to handle the error received from Coinbase."""
        print(f'Err: {err}')
    
    def _on_close(self, ws: 'websocket.WebSocketApp', close_status_code: int, close_msg: str) -> None:
        """This method is used to handle the close message received from Coinbase."""
        print("### closed ###")
    
    def _on_open(self, ws: 'websocket.WebSocketApp') -> None:
        """This method is used to handle the open message received from Coinbase."""
        # To receive feed messages, you must send a subscribe message or you are disconnected in 5 seconds.
        def run(*args):
            subscribe_message = {
                "type": "subscribe",
                "channels": self.channels,
                "product_ids": self.product_ids
            }
            ws.send(json.dumps(subscribe_message))
            print("Subscribed to channels:", self.channels)
        Thread(target=run).start()

    def run(self) -> None:
        """This method is used to run the websocket."""
        self._ws.run_forever()
    
    def shutdown(self) -> None:
        """This method is used to shutdown the websocket gracefully."""
        self._ws.close(1000, 'Shutdown')


if __name__ == '__main__':
    url = "wss://ws-feed.exchange.coinbase.com"
    channels = ["ticker"]
    product_ids = ["BTC-USD"]
    ingestor = CoinbaseDataIngestor(COINBASE_MKT_WEBSOCKET_API_SANDBOX, channels, product_ids)
    ingestor.run()