from sqlalchemy import(
    BigInteger,String,Column,
    DateTime,Uuid,ForeignKey,Text
)
from sqlalchemy.orm import relationship
from config.configs import SqlBase

class User(SqlBase):
    __tablename__ = "user"
    id = Column(
        Uuid,
        primary_key=True
    )
    name = Column(
        String(100)
    )
    subname = Column(
        String(100)
    )
    nickname = Column(
        String(100),
        unique=True,
        index=True
    )

class UserAuth(SqlBase):
    __tablename__ = "user_auth"
    id = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    email = Column(
        String(100),
        index=True
    )
    passwd = Column(
        String(255)
    )
    token = Column(
        Text
    )
    expirate = Column(
        DateTime
    )
    user_id = Column(
        Uuid,
        ForeignKey('user.id')
    )
    user = relationship(
        'User',
        cascade="all, delete"
    )


