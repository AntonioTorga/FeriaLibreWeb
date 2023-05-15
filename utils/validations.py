import filetype

def validate_img(img):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    ALLOWED_MIMETYPES = {'image/png', 'image/jpeg'}

    if img is None:
        return False
    if img.filename == '':
        return False
    ftype_guess = filetype.guess(img)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

