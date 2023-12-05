from datetime import datetime

from sqlalchemy import BigInteger, DateTime, func, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[int] = mapped_column()

    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column()
    datetime_create: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    role: Mapped["Role"] = relationship(back_populates="users")


class ParsedChannel(Base):
    __tablename__ = "parsed_channels"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column()

    parsed_channels_to_users: Mapped[list["UserToParsedChannel"]] = relationship(back_populates="parsed_channel")


class UserToParsedChannel(Base):
    __tablename__ = "users_to_parsed_channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    parsed_channel_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("parsed_channels.id"))
    parsed_channel_username: Mapped[str] = mapped_column()

    parsed_channel: Mapped[ParsedChannel] = relationship(back_populates="parsed_channels_to_users")


class ReceiverChannel(Base):
    __tablename__ = "receiver_channels"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    change_link: Mapped[bool] = mapped_column(default=True)
    link: Mapped[str] = mapped_column(nullable=True)
    postscript: Mapped[str] = mapped_column(nullable=True)
    deleted_key_words: Mapped[str] = mapped_column(nullable=True)


class Flow(Base):
    __tablename__ = "flow"

    id: Mapped[int] = mapped_column(primary_key=True)
    parsed_channel_id: Mapped[int] = mapped_column(BigInteger)
    receiver_channel_id: Mapped[int] = mapped_column(BigInteger)


class Media(Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column()
    file_id: Mapped[str] = mapped_column()
    media_group_id: Mapped[int] = mapped_column(BigInteger)
    caption: Mapped[str] = mapped_column(nullable=True)
    datetime_created: Mapped[datetime] = mapped_column(DateTime)


class Password(Base):
    __tablename__ = "password"

    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column()
    role_id: Mapped[int] = mapped_column()
