from werkzeug.security import generate_password_hash
from flask_login import current_user

from .models import *


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def get_area_by_id(area_id):
    return Area.query.filter_by(id=area_id).first()


def get_media_by_id(media_id):
    return Media.query.filter_by(id=media_id).first()


def get_media_by_area(area_id):
    area = Area.query.filter_by(id=area_id).first()
    return area.medias


def get_all_areas():
    return db.session.query(Area, User).filter(User.id == Area.user_id).order_by(Area.time_updated.desc()).all()
    # return Area.query.order_by(Area.time_updated.desc()).all()


def get_all_media_by_type(media_type):
    return Media.query.filter_by(media_type=media_type).all()
    # return Media.query.filter_by(media_type=media_type).all().order_by(Area.time_updated.desc())


def add_user(email, password):
    user = User.query.filter_by(email=email).first()
    result = False
    if not user:
        user_id = None
        if current_user:
            user_id = current_user.id
        db.session.add(User(email=email, password=generate_password_hash(
            password, method='sha256'), user_id=user_id))
        db.session.commit()
        result = True
    return result


def add_area(name, description, lat, long):
    result = False
    name = name.strip()
    area = Area.query.filter(func.lower(Area.name) == func.lower(name)).first()
    if not area:
        area = Area(name=name, description=description, user_id=current_user.id, lat=lat, long=long)
        db.session.add(area)
        db.session.commit()
        result = True
    return result


def add_media(name, path, media_type, area_id, long, lat): #lat lang was reversed
    result = False
    name = name.strip()
    path = path.strip()
    media = Media.query.filter(func.lower(Media.path) == func.lower(path)).first()
    area = get_area_by_id(area_id)
    if media is None and area is not None:
        media = Media(name=name, path=path, media_type=media_type,
                      area_id=area_id, user_id=current_user.id, lat=lat,
                      long=long)
        try:
            db.session.add(media)
            db.session.commit()
            result = True
        except:
            db.session.rollback()
    return result
