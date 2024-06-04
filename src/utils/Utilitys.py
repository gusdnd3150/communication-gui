from conf.logconfig import logger
import struct


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
        elif type == 'INT' or  type == 'SHORT' or type == 'LENGTH' :
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


def encodeDataToBytes(data, type, length):
    try:
        if type == 'STRING':
            padded_string = data.ljust(length, ' ')
            return padded_string.encode('utf-8')

        elif type == 'INT':
            value = 0
            if type(data) == str:
                value = int(data)
            else:
                value = data
            return value.to_bytes(4, byteorder='big')

        elif type == 'SHORT':
            if type(data) == str:
                value = int(data)
            else:
                value = data
            shortValue = value & 0xffff
            return shortValue.to_bytes(2, byteorder='big', signed=True)

        elif type == 'BYTE':
            if type(data) == int:
                decimal_value = data
                byte_array = decimal_value.to_bytes(1, byteorder='big')
                return byte_array
            else:  # 입력값이 문자열인 경우
                return data.encode('utf-8')

        elif type == 'DOUBLE':
            try:
                fval = float(data)
                return struct.pack('!d', fval)
            except ValueError:
                return struct.pack('!d', data)

    except Exception as e:
        logger.info(f'FreeCodec encodeDataToBytes Exception : {e}')
        return None