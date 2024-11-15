from prisma import Prisma

db = Prisma()

async def init_db():
    await db.connect()
