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


def encodeDataToBytes(data, type, length, pad=' '):
    try:
        if data is None:
            if type == 'STRING':
                data = ''
            elif type == 'INT' or type == 'SHORT' or type == 'DOUBLE':
                data = 1
            elif type == 'BYTE':
                data = bytearray([0x20] * length)
            elif type == 'BYTES': # 공백으로 초기화
                data = bytearray([0x20] * length)

        if type == 'STRING':
            padded_string = data.ljust(length, pad)
            return padded_string.encode('utf-8')

        elif type == 'INT':
            return data.to_bytes(4, byteorder='big')

        elif type == 'SHORT':
            shortValue = data & 0xffff
            return shortValue.to_bytes(2, byteorder='big', signed=True)

        elif type == 'BYTE' or type == 'VARIABLE_LENGTH' or type == 'BYTES':
           return data

        elif type == 'DOUBLE':
            try:
                fval = float(data)
                return struct.pack('!d', fval)
            except ValueError:
                return struct.pack('!d', data)

    except Exception as e:
        logger.info(f'Utilitys encodeDataToBytes Exception : {data}:{type}:{length}  {e}')
        return None


def castingValue(data, type):
    try:
        logger.info()


    except Exception as e:
        logger.info(f'castingValue Exception :: {e}')
