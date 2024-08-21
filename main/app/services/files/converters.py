from main.app.application.api.files.schemas import SFileInfo


def convert_file_status_document_to_dto(line: str) -> SFileInfo:
    line_list = line.split(' ')
    return SFileInfo(
        filename=line_list[0],
        status=line_list[1].rstrip()
    )