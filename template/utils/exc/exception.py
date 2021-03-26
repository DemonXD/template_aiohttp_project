class WrongFormatPicture(BaseException):
    """[summary]

    Args:
        Exception ([BaseException]): [
            need RGB picture, picture.shape(x, x, 3)
        ]
    """
    raise BaseException("Wrong value with the picture channel 3")
