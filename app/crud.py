from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

# Kép feltöltése
async def create_image(db: AsyncSession, image: schemas.ImageCreate):
    db_image = models.Image(**image.dict())
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image

# Összes kép lekérdezése
async def get_images(db: AsyncSession):
    result = await db.execute(select(models.Image))
    return result.scalars().all()

# E-mail feliratkozás
async def create_subscriber(db: AsyncSession, subscriber: schemas.SubscriberCreate):
    db_subscriber = models.Subscriber(**subscriber.dict())
    db.add(db_subscriber)
    await db.commit()
    await db.refresh(db_subscriber)
    return db_subscriber
