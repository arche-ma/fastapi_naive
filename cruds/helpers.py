import os

from slugify import slugify

from settings import settings


def save_image(
    image: bytes,
    artist_id: int,
    filename: str,
    static_dir=settings.static_dir,
) -> str:

    artist_dir = str(artist_id) + "/"
    filename = slugify(filename) + ".png"
    path = static_dir + "/" + artist_dir
    is_exist = os.path.exists(path)

    if not is_exist:
        os.makedirs(path)
    with open(path + filename, "wb") as file:
        file.write(image)
    return path + filename
