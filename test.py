from badx12 import Parser
import pandas as pd
import os

parser = Parser()


def collect_entries(document_body, file_name):
    """ Captures the fields in their approitate list"""
    for i, _ in enumerate(document_body):
        fields = document_body[i]['fields']
        for k, _ in enumerate(fields):
            entry = fields[k]
            name.append(entry["name"])
            description.append(entry["description"])
            required.append(entry["required"])
            min_length.append(entry["min_length"])
            max_length.append(entry["max_length"])
            content.append(entry["content"])
            file.append(file_name)


with open(r'C:\Users\e149087\Documents\Data Lake Project\small_sample.edi', 'r', encoding='utf-8-sig') as f:
    document = parser.parse_document(f.read())

    parse = document.to_dict()

    body = parse['document']['interchange']['body'][0]['body'][0]['body']

    name = []
    description = []
    required = []
    min_length = []
    max_length = []
    content = []
    file = []

    collect_entries(body)

    data = {
        'name': name,
        'description': description,
        'required': required,
        'min_length': min_length,
        'max_length': max_length,
        'content': content,
        'file': file
    }

    push = pd.DataFrame(data)

    print()
