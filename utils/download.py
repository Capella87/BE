import io
import mimetypes
import urllib
from pathlib import Path, PureWindowsPath, PurePosixPath
from typing import Any

from django.http import HttpResponse

from competition.models import Competition

# TODO : Convert these file to respond the convenient pathlib library

# For Windows
def csv_download_windows(submission_path: str, base_dir: str | bytes) -> (str, str):
    base_dir = base_dir.replace("\\submission", "")
    csv_path = str(submission_path).split('uploads\\', 1)[1]
    filename = csv_path.split('\\', 2)[2]
    filename = urllib.parse.quote(filename.encode('utf-8'))
    filepath = base_dir + '\\uploads\\' + csv_path

    return filename, filepath


# For Unix or Unix-compatible operating systems
def csv_download_nix(submission_path: str, base_dir: str | bytes) -> (str, str):
    base_dir = base_dir.replace("/submission", "")

    csv_path = str(submission_path).split('uploads/', 1)[1]
    filename = csv_path.split('/', 2)[2]
    filename = urllib.parse.quote(filename.encode('utf-8'))
    filepath = base_dir + '/uploads/' + csv_path

    return filename, filepath


def ipynb_download_windows(submission_path: str, base_dir: str | bytes) -> (str, str):
    base_dir = base_dir.replace("\\submission", "")

    ipynb_path = str(submission_path).split('uploads\\', 1)[1]
    filename = ipynb_path.split('\\', 2)[2]
    filename = urllib.parse.quote(filename.encode('utf-8'))
    filepath = base_dir + '\\uploads\\' + ipynb_path

    return filename, filepath


def ipynb_download_nix(submission_path: str, base_dir: str | bytes) -> (str, str):
    base_dir = base_dir.replace("/submission", "")

    ipynb_path = str(submission_path).split('uploads/', 1)[1]
    filename = ipynb_path.split('/', 2)[2]
    filename = urllib.parse.quote(filename.encode('utf-8'))
    filepath = base_dir + '/uploads/' + ipynb_path

    return filename, filepath


# Get mime type
def get_mimetype(filepath: Path) -> str:
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)

    return mime_type


# Attach HTTP header
def get_attachment_response(filepath: Path, mime_type: str) -> HttpResponse:
    # Open the file for reading content
    path = open(filepath, 'rb')
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % str(filepath.name)

    return response

