# bb-middleware (wip)

Middleware to calculate and cache blockchain and accounts state given block events.

## development environment
python 3.8.2
pip 20.0.2
ubuntu 20.04

## setup
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

To have a better visualization pipe it with `json_pp` (if available)
```bash
./cli.py <blockchain.json> | json_pp
# or
./cli.py <blockchain.json> --median | json_pp
```

## rest server

Implemented using flask. No authentication, data check, docs, flask blueprint.
It's plain and simpe with the purpose of just outputing some data for any incoming request.

The server is running in dev mode with the `mock/mockchain.json`, but new accounts as well as new blocks could be added to the end of the chain.

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

There is fake implementation for the event listener.
There is nothing to read, however wiring up would be seamless as it is.

## tests

```bash
make test
```

## to-dos
- linting
- make some integration tests
