# bb-middleware (wip)

Middleware to calculate and cache blockchain and accounts state given block events.

## development environment
python 3.8.2

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

```
make run-rest-server
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

## tests

```bash
make test
```

## to-dos
- linting
- api layer (rest, event listener)
- comments in the code
- proper README
- make some integration tests
