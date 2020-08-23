# bb-middleware

Middleware to calculate and cache blockchain and accounts state given block events.

## dev environment
* python 3.8.2
* pip 20.0.2
* ubuntu 20.04
* vim 8.1.2269

## setup
To install the dependencies run the following command:

```bash
make setup
```

## cli tool

Play a block chain and outputs the overall balance.
```bash
./cli.py -h
```

To run and retrieve the balance:
```bash
./cli.py <blockchain.json>
```

To run and retrieve the median:
```bash
./cli.py <blockchain.json> --median
```

To have a better visualization pipe it with `json_pp` (if available).
```bash
./cli.py <blockchain.json> | json_pp
# or
./cli.py <blockchain.json> --median | json_pp
```

## rest server

Implemented using flask. No authentication, data check, docs, flask blueprint.
It's plain and simpe with the purpose of just outputing some data for any incoming http request.

The server is running in dev mode with the `mock/mockchain.json` loaded in, but new blocks can be added to the end of the chain as it should.

```bash
make run-rest-server
```

To run without the mock file, please set the `MOCK` env var to false as below:
```bash
MOCK=false make run-rest-server
```

### api reference
#### `POST /chain`
add a new block to a chain

payload: `{ number: int, balances: arr, transfers: arr, hash: str, prevhash: str }`

#### `GET /chain`
retrieves all the blocks in a chain

response: `[{ number: int, balances: arr, transfers: arr, hash: str, prevhash: str }]`

#### `GET /block/<block_hash>`
retrieves the block

params: `block_hash`: str

response: `{ number: int, balances: arr, transfers: arr, hash: str, prevhash: str }`

#### `POST /account/balance`
set a new balance

payload: `{ address: str, amount: int }`

#### `GET /account/balance`
retrieves all the balances

response: `{ "foo": float, "bar": float, ... }`

#### `GET /account/balance/<address>`
retrieves the balance from an address

params: `address`: str

response: `amount`: float

#### `GET /account/median`
retrieves all the medians

response: `{ "foo": float, "bar": float, ... }`

#### `GET /account/median/<address>`
retrieves the median from an address

params: `address`: str

response: `median`: float

## event listener

There is a fake implementation for the event listener in place, just for demo purposes.
There is nothing to read, however wiring up would be seamless as it is.

## tests
Unit and integration tests build over the `handler` files.

```bash
make test
```

## lint

```bash
make lint
```

## to-do

* complex integration tests.
* more tests for the revert of transfers once such reverts should not happen on the median calculation.
* an actual cache abstraction for `storage/GenericStorage`. `RedisStorage` was planned but not executed due to lack of timing.
* with `RedisStorage` abstraction in place, a docker compose would be done to set up redis as well as the event listener and the rest api.
* dependency injection lib helper.
* type-checking usage.
