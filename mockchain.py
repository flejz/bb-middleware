import hashlib
import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# Percentage of transfers that should be reused when creating a new block with
# sibilings.
TRANSFER_REUSE_RATIO = 0.5


def hexhash(seed: str) -> str:
    seed_bytes = seed.encode("utf8")
    digest = hashlib.sha224(seed_bytes).hexdigest()

    return f"0x{digest[:6]}"


def generate_chain_with_forks(
    chain_description: "ChainDescription"
) -> Tuple[List["SealedBlock"], int]:
    """ Return a list of `SealedBlock`s.

    The last block in the list is the highest and corresponds to the
    `chain_description.target_height`.

    The list does not contain *just* the canonical chain, but all blocks from
    all forks.
    """
    genesis = generate_genesis_block(qty_accounts=chain_description.qty_accounts)
    all_blocks = [genesis]
    current_head = genesis
    track_sibillings: Dict[int, List[SealedBlock]] = defaultdict(list)
    longest_revert = 0
    current_revert = 0

    while current_head.number < chain_description.target_height:

        if (
            # The genesis block can not be reverted.
            current_head.parent_block is not None
            and random.random() <= chain_description.revert_probability
        ):
            # Reverts are allowed to accumulate. E.g.
            #
            # all_blocks    = [g, b1, b2, b3]
            # longest head  =             ^
            # first revert  =         ^
            # second revert =     ^
            #
            # This allows for forks of a depth greater than `1`.
            current_head = current_head.parent_block
            current_revert += 1
            longest_revert = max(current_revert, longest_revert)
        else:
            # New blocks are always generated based on the `current_head`. This
            # will pick up from the previous iteration, which may have been an
            # accumulated revert. Continuing the example above:
            #
            # all_blocks    = [g, b1, b2, b3, b2', b3']
            # new block     =                 ^
            # new block'    =                      ^
            #
            # At this point there is a fork with depth `2` and the chain is:
            #
            #                   v--- current head
            #    g - b1 - b2' - b3'
            #         |
            #         +-- b2  - b3
            #
            current_head = generate_new_block(
                current_head,
                track_sibillings[current_head.number],
                chain_description.qty_transfers_per_block,
            )

            all_blocks.append(current_head)
            track_sibillings[current_head.number].append(current_head)
            current_revert = max(0, current_revert - 1)

    return all_blocks, longest_revert


def generate_genesis_block(qty_accounts: int) -> "SealedBlock":
    initial_accounts = tuple(
        Account(address=hexhash(str(address_seed)), balance=random.randint(1, 100))
        for address_seed in range(qty_accounts)
    )

    genesis = SealedBlock(parent_block=None, accounts=initial_accounts, transfers=tuple())

    return genesis


def generate_new_block(
    parent_block: "SealedBlock", sibilings: List["SealedBlock"], qty_transfers: int
) -> "SealedBlock":
    pending = PendingBlock.from_sealed_as_parent(parent_block)

    if sibilings:
        qty_reuse_transfers = math.ceil(qty_transfers * TRANSFER_REUSE_RATIO)

        all_transfers = [transfer for sibiling in sibilings for transfer in sibiling.transfers]
        random.shuffle(all_transfers)
        transfer_iter = iter(all_transfers)

        # Because the transfers can be done in a different order, a random
        # transfer from the previous iteration may not be valid anymore. This
        # keeps track of how many transfers could actually be reused.
        qty_performed_transfers = 0

        for _ in range(qty_reuse_transfers):
            candidate = next(transfer_iter)

            is_transfer_valid = pending.balances[candidate.sender] >= candidate.amount
            if is_transfer_valid:
                pending.transfer(candidate.sender, candidate.receiver, candidate.amount)
                qty_performed_transfers += 1

        pending.generate_transfers(qty_transfers - qty_performed_transfers)
    else:
        pending.generate_transfers(qty_transfers)

    return SealedBlock.from_pending(pending)


@dataclass(frozen=True)
class ChainDescription:
    """Configuration for the generated chain."""

    target_height: int
    revert_probability: float
    qty_accounts: int
    qty_transfers_per_block: int


@dataclass(frozen=True, eq=True)
class TransferEvent:
    sender: str
    receiver: str
    amount: int


@dataclass(frozen=True, eq=True)
class Account:
    address: str
    balance: int


@dataclass(frozen=True, eq=True)
class SealedBlock:
    parent_block: Optional["SealedBlock"]
    accounts: Tuple[Account, ...]
    transfers: Tuple[TransferEvent, ...]
    number: int = field(init=False)

    def __post_init__(self) -> None:
        if self.parent_block is None:
            number = 0
            assert not self.transfers, "genesis block must not have transfers."
        else:
            number = self.parent_block.number + 1

        object.__setattr__(self, "number", number)

    @staticmethod
    def from_pending(pending_block: "PendingBlock") -> "SealedBlock":
        return SealedBlock(
            parent_block=pending_block.parent_block,
            accounts=tuple(
                Account(address, balance) for address, balance in pending_block.balances.items()
            ),
            transfers=tuple(pending_block.transfers),
        )

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "number": self.number,
            "hash": hash(self),
            "prevhash": hash(self.parent_block),
            "transfers": [
                {
                    "sender": transfer.sender,
                    "receiver": transfer.receiver,
                    "amount": transfer.amount,
                }
                for transfer in self.transfers
            ],
        }

        if self.number == 0:
            data["balances"] = {account.address: account.balance for account in self.accounts}

        return data


@dataclass
class PendingBlock:
    parent_block: SealedBlock
    balances: Dict[str, int]
    transfers: List["TransferEvent"]

    @staticmethod
    def from_sealed_as_parent(sealed_block: SealedBlock) -> "PendingBlock":
        balances = {account.address: account.balance for account in sealed_block.accounts}

        # The length of the containers would only change if there is a address
        # collision, meaning there is more than one entry for the same account
        # in the sealed block.
        msg = "Duplicated account detected."
        assert len(balances) == len(sealed_block.accounts), msg

        return PendingBlock(parent_block=sealed_block, balances=balances, transfers=list())

    def generate_transfers(self, qty_transfers: int) -> None:
        """Generates random transfers."""

        addresses = list(self.balances.keys())
        for _ in range(qty_transfers):
            sender = None
            while sender is None:
                candidate = random.choice(addresses)
                sender_balance = self.balances[candidate]
                if sender_balance > 0:
                    sender = candidate

            receiver = None
            while receiver is None:
                candidate = random.choice(addresses)
                if sender != candidate:
                    receiver = candidate

            amount = random.randint(1, sender_balance)

            self.transfer(sender, receiver, amount)

    def transfer(self, sender_address: str, receiver_address: str, amount: int) -> None:
        sender_new_balance = self.balances[sender_address] - amount
        assert sender_new_balance >= 0, "sender must have enough balance for the transfer."

        self.balances[sender_address] = sender_new_balance
        self.balances[receiver_address] = self.balances[receiver_address] + amount

        self.transfers.append(TransferEvent(sender_address, receiver_address, amount))


def main():
    random.seed(43)
    chain_description = ChainDescription(
        target_height=10, revert_probability=0.5, qty_accounts=100, qty_transfers_per_block=10
    )
    chain, longest_revert = generate_chain_with_forks(chain_description)
    serialized_blocks = [block.to_dict() for block in chain]

    unique_transfers = chain_description.qty_transfers_per_block * chain_description.target_height
    total_transfers = sum(len(block.transfers) for block in chain)

    print(json.dumps(serialized_blocks, indent=4, sort_keys=True))
    print(f"blocks: {len(chain)} max reverted: {longest_revert} last hash: {hash(chain[-1])}")
    print(f"total transfers: {total_transfers} unique transfers: {unique_transfers}")


if __name__ == "__main__":
    main()
