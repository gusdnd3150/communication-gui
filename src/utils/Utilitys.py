from conf.logconfig import logger


def decodeBytes( bytes, type):
    returnData = None
    try:
        if type == 'STRING':
            returnData = bytes.decode('utf-8-sig').strip()
        elif type == 'INT':
            returnData = int.from_bytes(bytes, byteorder='big')
        elif type == 'SHORT':
            returnData = int.from_bytes(bytes, byteorder='big', signed=True)
        elif type == 'BYTE' or type == 'BYTES':
            returnData = bytes
    except Exception as e:
        logger.info(f'FreeCodec parsingBytes Exception : {e}')

    return returnData


def encodeToBytes(data, type):
    try:
        if type == 'STRING':
            return data
        elif type == 'INT':
            int_data = int(data)
            return int_data.to_bytes((int_data.bit_length() + 7) // 8 or 1, byteorder='big')
        elif type == 'SHORT':
            short_data = int(data)
            return short_data.to_bytes(2, byteorder='big', signed=True)
        elif type == 'BYTE':
            byte_data = int(data, 16)  # 16진수 문자열을 정수로 변환
            return bytes([byte_data])
        elif type == 'BYTES':
            return bytes.fromhex(data)
        else:
            raise ValueError(f"Unsupported type: {type}")
    except Exception as e:
        logger.info(f'FreeCodec encodeToBytes Exception : {e}')
        return None