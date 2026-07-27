import traceback

from conf.logconfig import logger
import struct


# RECIVE BODY로 넘어오는 데이터를 타입/길이 바탕으로 파싱
def decodeBytesToType( bytes, type):
    returnData = None
    try:
        if type == 'STRING':
            returnData = bytes.decode('utf-8-sig').strip()
        elif type == 'INT':
            returnData = int.from_bytes(bytes, byteorder='big')
        elif type == 'INT_LE':
            returnData = int.from_bytes(bytes, byteorder='little')
        elif type == 'SHORT':
            returnData = int.from_bytes(bytes, byteorder='big', signed=True)
        elif type == 'SHORT_LE':
            returnData = int.from_bytes(bytes, byteorder='little', signed=True)
        elif type == 'FLOAT':
            if len(bytes) != 4:
                raise ValueError("FLOAT type requires 4 bytes")
            returnData = struct.unpack('!f', bytes)[0]  # big-endian float
        elif type == 'FLOAT_LE':
            if len(bytes) != 4:
                raise ValueError("FLOAT_LE type requires 4 bytes")
            returnData = struct.unpack('<f', bytes)[0]  # little-endian float
        elif type == 'DOUBLE':
            if len(bytes) != 8:
                raise ValueError("DOUBLE type requires 8 bytes")
            returnData = struct.unpack('!d', bytes)[0]  # big-endian double
        elif type == 'DOUBLE_LE':
            if len(bytes) != 8:
                raise ValueError("DOUBLE_LE type requires 8 bytes")
            returnData = struct.unpack('<d', bytes)[0]  # little-endian double
        elif type == 'BYTE' or type == 'BYTES' or type == 'VARIABLE_LENGTH':
            returnData = bytes
    except Exception as e:
        logger.error(f'Utilitys decodeBytesToType  Exception : {e}')

    return returnData


def decodeMsgKeyVal(data, type):
    try:
        if type == 'STRING':
            return data
        elif type == 'INT' or  type == 'SHORT' or type == 'LENGTH' or type =='INT_LE' or type =='SHORT_LE' :
            int_data = int(data)
            return int_data
        elif type == 'BYTE':
            byte_data = strHexToByte(data)
            return bytes([byte_data])
        elif type == 'BYTES':
            return strHexToBytes(data)
        else:
            return None
    except Exception as e:
        logger.error(f'Utilitys decodeMsgKeyVal Exception : {e}')
        return None


# 16진수 문자열을 바이트로 변환 '0x00'
def strHexToByte(hexStr):
    return int(hexStr, 16).to_bytes(1, byteorder='big')

# 16진수 문자열을 바이트로 변환 ('0x00 0x01 0x03' 등 공백으로 구분된 Hex 문자열)
def strHexToBytes(hexStrs):
    if not hexStrs:
        return b''
    return bytes(int(hex_str, 16) for hex_str in hexStrs.split())


# SEND BODY 로 전송되는 타입/길이 바탕으로 전문 파싱
def encodeDataToBytes(data, type, length, pad=' '):
    try:
        if data is None:
            if type == 'STRING' or type == 'VARIABLE_LENGTH' or type == 'BASE64_DECMALS':
                data = ''
            elif type == 'INT' or type == 'SHORT' or type == 'DOUBLE' or type == 'FLOAT':
                data = 0
            elif type == 'INT_LE' or type == 'SHORT_LE' or type == 'DOUBLE_LE' or type == 'FLOAT_LE':
                data = 0
            elif type == 'BYTE' or type == 'BYTES':
                data = bytearray([0x20] * length)

        if length is None:
            if type == 'STRING':
                length = len(data)
            elif type == 'INT' or type == 'INT_LE':
                length = 4
            elif type == 'SHORT' or type == 'SHORT_LE':
                length = 2
            elif type == 'DOUBLE'or type == 'DOUBLE_LE':
                length = 8
            elif type == 'FLOAT' or type == 'FLOAT_LE':
                length = 4

        length = int(length)


        if type == 'STRING':
            padded_string = str(data).rjust(length, pad)
            return padded_string.encode('utf-8')

        elif type == 'INT':
            return data.to_bytes(4, byteorder='big')

        elif type == 'INT_LE':
            return data.to_bytes(4, byteorder='little')

        elif type == 'SHORT':
            shortValue = data & 0xffff
            return shortValue.to_bytes(2, byteorder='big', signed=True)

        elif type == 'SHORT_LE':
            shortValue = data & 0xffff
            return shortValue.to_bytes(2, byteorder='little', signed=True)

        elif type == 'BYTE' or type == 'BYTES' :
           return data

        elif type == 'VARIABLE_LENGTH' or type == 'BASE64_DECMALS':
           return data.encode('utf-8')

        elif type == 'FLOAT':
            try:
                fval = float(data)
                return struct.pack('!f', fval)
            except ValueError:
                return struct.pack('!f', data)

        elif type == 'FLOAT_LE':
            try:
                fval = float(data)
                return struct.pack('<f', fval)
            except ValueError:
                return struct.pack('<f', data)

        elif type == 'DOUBLE':
            try:
                fval = float(data)
                return struct.pack('!d', fval)
            except ValueError:
                return struct.pack('!d', data)

        elif type == 'DOUBLE_LE':
            try:
                fval = float(data)
                return struct.pack('<d', fval)
            except ValueError:
                return struct.pack('<d', data)

    except Exception as e:
        logger.error(f'Utilitys encodeDataToBytes Exception : {data}:{type}:{length}  {e}')
        return None

