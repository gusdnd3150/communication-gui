from conf.logconfig import logger


def decodeBytesToType( bytes, type):
    returnData = None
    try:
        if type == 'STRING':
            returnData = bytes.decode('utf-8-sig').strip()
        elif type == 'INT':
            returnData = int.from_bytes(bytes, byteorder='big')
        elif type == 'SHORT':
            returnData = int.from_bytes(bytes, byteorder='big', signed=True)
        elif type == 'BYTE' or type == 'BYTES' or type == 'VARIABLE_LENGTH':
            returnData = bytes
    except Exception as e:
        logger.info(f'FreeCodec parsingBytes Exception : {e}')

    return returnData


def encodeToBytes(data, type):
    try:
        if type == 'STRING':
            return data
        elif type == 'INT' or  type == 'SHORT' :
            int_data = int(data)
            return int_data
        elif type == 'BYTE':
            byte_data = int(data, 16)  # 16진수 문자열을 정수로 변환
            return bytes([byte_data])
        elif type == 'BYTES':
            return bytes.fromhex(data)
        else:
            return None
    except Exception as e:
        logger.info(f'FreeCodec encodeToBytes Exception : {e}')
        return None