loop = {}


async def get_loop(chat_id: int) -> int:
    lop = loop.get(chat_id, 0)
    return lop

async def set_loop(chat_id: int, mode: int):
    loop[chat_id] = mode