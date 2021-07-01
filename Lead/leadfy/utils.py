import uuid


def generate_ref_code():
    code = str(uuid.uuid4()).replace('-', '')[:5]
    return code
