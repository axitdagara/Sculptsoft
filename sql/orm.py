from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:123456789@localhost:5432/library_db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# new_user = User(
#     name="Harsh",
#     email="harsh@gmail.com"
# )

# session.add(new_user)
# session.commit()


# new_user = User(
#     name="Rahul",
#     email="rahul@gmail.com"
# )


# session.add(new_user)
# session.commit()

# print("User Added")

users = session.query(User).all()

for user in users:
    print(user.name)
    
    
print("User detials")



# user = session.query(User).filter_by(id=1).first()

# user.name = "Rahul Sharma"

# session.commit()



user = session.query(User).filter_by(id=1).first()

session.delete(user)

session.commit()
session.close()