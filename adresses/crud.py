from adresses.schemas import CreateAddress
from core.models.users import Address
from core.repository import repo


async def list_addrs() -> list[Address]:
    addrs = await repo.list(model=Address)
    return list(addrs)


async def get_addr(model: Address, addr_id: int) -> Address | None:
    return await repo.get(model=model, ref_id=addr_id)


async def create_addr(addr_in: CreateAddress) -> Address:
    addr = Address(**addr_in.model_dump())
    await repo.add(obj=addr)
    return addr
