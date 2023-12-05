

def add_media_list(media_group_id: str, type_media: str, file_id: str):
    with open(f"media_list/media_files_{media_group_id}.txt", "a", encoding="UTF-8") as file:
        file.write(f"{type_media}__{file_id}\n")


def read_media_list(path: str):
    media = []
    with open(path, "r", encoding="UTF-8") as file:
        for row in file:
            type_, data = row.split("__")
            data = data[:-2]
            media.append({"type": type_, "data": data})
    return media
