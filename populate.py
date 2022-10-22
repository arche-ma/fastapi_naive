import csv

from sqlalchemy.orm import Session

from db import SessionLocal
from models import Artist, Artwork, Tag, User

db_session = SessionLocal()


def from_csv_to_db(session: Session, filename: str, model):
    with open(filename, "r") as csv_file:
        with db_session as session:
            data = csv.DictReader(csv_file)
            for line in data:
                line = {
                    key: True if v == "True" else v
                    for (key, v) in line.items()
                }
                print(line)
                session.add(model(**line))
            session.commit()


if __name__ == "__main__":
    csv_files = ["artists.csv", "artworks.csv", "tags.csv", "users.csv"]
    models = [Artist, Artwork, Tag, User]
    parameters = [
        {"session": db_session, "filename": name, "model": model}
        for (name, model) in zip(csv_files, models)
    ]
    for parameter in parameters:
        from_csv_to_db(**parameter)
