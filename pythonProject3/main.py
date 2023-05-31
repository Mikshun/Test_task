import shutil

from fastapi import FastAPI, UploadFile, File, Request
from uuid import uuid1
from secrets import token_hex
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from os import mkdir
from os.path import  isdir
import ffmpeg

app = FastAPI(title="Test_Api")

engine = create_engine('postgresql+psycopg2://admin:admin@pg_user/users')

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    uuid = Column(String)
    token = Column(String)

    def __repr__(self):
        return f"{self.name},{self.uuid},{self.token}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Media(Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    record = Column(String)
    user_id = Column(Integer)

    def __repr__(self):
        return f"{self.record},{self.user_id}"

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base.metadata.create_all(bind=engine)


# noinspection PyArgumentList

@app.get('/')
def get_all(request: Request):
    return session.query(User).all()
    # return request.url.hostname


@app.post('/')
def create(name: str):
    user_uuid = str(uuid1())
    user_token = token_hex(16)
    new_record = User(
        name=name,
        uuid=user_uuid,
        token=user_token
    )
    session.add(new_record)
    session.commit()
    return {'uuid': user_uuid, 'token': user_token}


@app.post('/record')
def loader(uuid, token, request: Request, file: UploadFile = File(...)):
    check = session.query(User).filter(User.uuid == uuid and User.token == token).first()
    if check is not None:
        user_id = check.id
        file_uuid = str(uuid1())
        type = str(file.filename).split('.')
        if type[1] != 'wav':
            raise HTTPException(400, detail='Формат файла должен быть wav')

        if not isdir('static'):
            mkdir('static')

        with open(f'./static/{file_uuid}.wav', "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        song = ffmpeg.input(f'./static/{file_uuid}.wav')
        song = ffmpeg.output(song, f'./static/{file_uuid}.mp3')
        ffmpeg.run(song)

        new_record = Media(
            record=file_uuid,
            user_id=user_id
        )
        session.add(new_record)
        session.commit()

        return f"http://{request.url.hostname}:{request.url.port}/record?uuid={file_uuid}&user={user_id}"
    return HTTPException(400, detail='В базе данных нет пользователя с данными параметрами')


@app.get('/record')
def downoload(uuid, user: int):
    user_obj = session.query(Media).filter(Media.user_id == user and Media.record == uuid).first()
    if user_obj is not None:
        return FileResponse(path=f'./static/{uuid}.mp3', filename='music.mp3')
    return HTTPException(400, detail='Данная запись не найдена в базе данных')
