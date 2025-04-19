from sqlmodel import Session, create_engine, select

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)