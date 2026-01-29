from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy import create_engine, inspect, select, update


class Base(DeclarativeBase):
    pass


class Users(Base):

    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str]
    is_subscribed: Mapped[bool] = mapped_column(default=True)


class DataBase:

    __URL = "sqlite:///database.db"

    @staticmethod
    def __create_table(engine):
        Base.metadata.create_all(engine)

    @staticmethod
    def __check_table(engine):
        inspector = inspect(engine)

        if not inspector.has_table("Users"):
            DataBase.__create_table(engine)

    @staticmethod
    def add_new_user(chat_id: int, first_name: str, last_name: str, username: str):
        engine = create_engine(DataBase.__URL)

        DataBase.__check_table(engine)

        with Session(engine) as session:
            get_current_user_query = select(Users).filter_by(chat_id=chat_id)
            result = session.execute(get_current_user_query)
            current_user = result.first()
            if current_user is None:
                new_user = Users(chat_id=chat_id, first_name=first_name, last_name=last_name, username=username)
                session.add(new_user)
                session.commit()
        
        engine.dispose()

    @staticmethod
    def get_user_name(chat_id: int) -> str:
        engine = create_engine(DataBase.__URL)

        with Session(engine) as session:
            query = select(Users.first_name).filter_by(chat_id=chat_id)
            result = session.execute(query)
            name = result.scalar_one()

        engine.dispose()
        return name
    
    @staticmethod
    def get_subscribers() -> list[dict[str, int, str]]:
        engine = create_engine(DataBase.__URL)

        with Session(engine) as session:
            get_subscribers_query = select(Users.chat_id, Users.first_name).filter_by(is_subscribed=True)
            result = session.execute(get_subscribers_query)
            subscribers = result.mappings().all()

        engine.dispose()
        return subscribers
    
    @staticmethod
    def change_subscription(chat_id: int, is_subscription: bool) -> str:
        engine = create_engine(DataBase.__URL)

        with Session(engine) as session:
            unsubscribe_query = update(Users).filter_by(chat_id=chat_id).values(is_subscribed=is_subscription).returning(Users.first_name)
            result = session.execute(unsubscribe_query)
            name = result.scalar_one()
            session.commit()

        engine.dispose()
        return name
