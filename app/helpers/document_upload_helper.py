ALLOWED_DOCUMENT_EXTENSIONS = {"pdf", "doc", "docx", "txt"}


def allowed_document_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_DOCUMENT_EXTENSIONS
    )