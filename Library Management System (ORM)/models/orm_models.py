from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship
from config.db import Base


class BookORM(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    available = Column(Boolean, nullable=False, default=True)

    borrow_entries = relationship("BorrowHistoryORM", back_populates="book", cascade="all, delete-orphan")


class UserORM(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=True)
    borrow_limit = Column(Integer, nullable=False, default=3)
    borrow_days = Column(Integer, nullable=False, default=14)
    fine_per_day = Column(Numeric(10, 2), nullable=False, default=2.00)

    borrow_entries = relationship("BorrowHistoryORM", back_populates="user", cascade="all, delete-orphan")
    role_assignments = relationship("UserRoleORM", back_populates="user", cascade="all, delete-orphan")

    @property
    def roles(self) -> list["RoleORM"]:
        return [assignment.role for assignment in self.role_assignments if assignment.role is not None]

    @property
    def role(self) -> str:
        role_names = [role.name for role in self.roles]
        if "admin" in role_names:
            return "admin"
        return role_names[0] if role_names else "user"


class RoleORM(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    user_assignments = relationship("UserRoleORM", back_populates="role", cascade="all, delete-orphan")


class UserRoleORM(Base):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_roles_user_id_role_id"),)

    user_role_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), nullable=False)

    user = relationship("UserORM", back_populates="role_assignments")
    role = relationship("RoleORM", back_populates="user_assignments")


class BorrowHistoryORM(Base):
    __tablename__ = "borrow_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id", ondelete="CASCADE"), nullable=False)
    borrowed_on = Column(Date, nullable=False)
    due_on = Column(Date, nullable=False)
    returned_on = Column(Date, nullable=True)
    fine = Column(Numeric(10, 2), nullable=False, default=0.00)

    user = relationship("UserORM", back_populates="borrow_entries")
    book = relationship("BookORM", back_populates="borrow_entries")
