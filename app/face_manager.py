import face_recognition
import numpy as np
from models import User
from database import db_session
import os

def add_user_from_image(username, image_path):
    session = db_session()
    try:
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            user = User(username=username, face_encoding=np.array(face_encodings[0]).tobytes())
            session.add(user)
            session.commit()
        else:
            print(f"No faces found in the image {image_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

def authenticate_user_from_image(image_path):
    session = db_session()
    try:
        unknown_image = face_recognition.load_image_file(image_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)
        if not unknown_face_encodings:
            print("No faces found in the image.")
            return None
        
        for user in session.query(User).all():
            known_face_encoding = np.frombuffer(user.face_encoding, dtype=np.float64)
            results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
            if results[0]:
                return user.username
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()
    return None

def user_exists_by_name(username):
    session = db_session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user is not None

def user_exists_by_face(image_path):
    session = db_session()
    try:
        unknown_image = face_recognition.load_image_file(image_path)
        unknown_face_encodings = face_recognition.face_encodings(unknown_image)[0]
        
        for user in session.query(User).all():
            known_face_encoding = np.frombuffer(user.face_encoding, dtype=np.float64)
            results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings)
            if results[0]:
                return True
    except Exception as e:
        print(f"An error occurred while trying to find a face match: {e}")
    finally:
        session.close()
    return False
