
from fastapi import APIRouter, HTTPException

from starlette import status

from adresses.schemas import AddressSchema, CreateAddress
from core.models.users import Address
from adresses import crud

router = APIRouter(prefix="/addrs", tags=["addresses"])


@router.get("/", response_model=list[AddressSchema])
async def list_addrs():
    return await crud.list_addrs()


@router.post("/", response_model=AddressSchema)
async def create_addr(addr: CreateAddress):
    return await crud.create_addr(addr_in=addr)


@router.get("/{addr_id}/", response_model=AddressSchema)
async def get_single_addr(addr_id: int):
    addr = await crud.get_addr(model=Address, addr_id=addr_id)
    if not addr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return addr

