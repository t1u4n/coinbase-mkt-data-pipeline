import websocket
import json
from threading import Thread
from typing import List
from dotenv import load_dotenv
import os
from kafka import KafkaProducer

load_dotenv()

COINBASE_MKT_WEBSOCKET_API_PROD = 'wss://ws-feed.exchange.coinbase.com'
COINBASE_MKT_WEBSOCKET_API_SANDBOX = 'wss://ws-feed-public.sandbox.exchange.coinbase.com'
KAFKA_URLS = os.getenv('KAFKA_URL').split(',')


class CoinbaseDataIngestor:
    """This class is used to ingest data from Coinbase."""

    def __init__(self, url: str, channels: List[str], product_ids: List[str]):
        """Constructor of CoinbaseDataIngestor."""
        self._url = url
        self._channels = channels
        self._product_ids = product_ids
        self._ws = websocket.WebSocketApp(self._url,
                                         on_open=self._on_open,
                                         on_message=self._on_message,
                                         on_error=self._on_error,
                                         on_close=self._on_close)
        self._kafka_producer = KafkaProducer(bootstrap_servers = KAFKA_URLS)
    
    def _on_message(self, ws: 'websocket.WebSocketApp', msg: str) -> None:
        """This method is used to handle the message received from Coinbase."""
        payload = json.loads(msg)
        if 'type' in payload and payload['type'] == 'ticker':
            topic = payload['product_id']
            self._kafka_producer.send(topic, msg.encode('utf-8'))
    
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
                "channels": self._channels,
                "product_ids": self._product_ids
            }
            ws.send(json.dumps(subscribe_message))
            print("Subscribed to channels:", self._channels)
        Thread(target=run).start()

    def run(self) -> None:
        """This method is used to run the websocket."""
        self._ws.run_forever()
    
    def shutdown(self) -> None:
        """This method is used to shutdown the websocket gracefully."""
        self._ws.close(1000, 'Shutdown')
        self._kafka_producer.close(10)


if __name__ == '__main__':
    # Enable traces for websocket client if need to debug
    # websocket.enableTrace(True)
    url = "wss://ws-feed.exchange.coinbase.com"
    channels = ["ticker"]
    product_ids = ["BTC-USD"]
    ingestor = CoinbaseDataIngestor(COINBASE_MKT_WEBSOCKET_API_SANDBOX, channels, product_ids)
    ingestor.run()