import traceback

from conf.logconfig import logger
import struct
import requests

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
        logger.error(f'FreeCodec parsingBytes Exception : {e}')

    return returnData


def encodeToBytes(data, type):
    try:
        if type == 'STRING':
            return data
        elif type == 'INT' or  type == 'SHORT' or type == 'LENGTH' :
            int_data = int(data)
            return int_data
        elif type == 'BYTE':
            byte_data = int(data, 16).to_bytes(1, byteorder='big')  # 16진수 문자열을 바이트로 변환
            return bytes([byte_data])
        elif type == 'BYTES':
            return bytes.fromhex(data)
        else:
            return None
    except Exception as e:
        logger.error(f'FreeCodec encodeToBytes Exception : {e}')
        return None


def encodeDataToBytes(data, type, length, pad=' '):
    try:
        # print(f'encodeDataToBytes {data},{type},{length}')
        if data is None:
            if type == 'STRING':
                data = ''
            elif type == 'INT' or type == 'SHORT' or type == 'DOUBLE':
                data = 1
            elif type == 'BYTE':
                data = bytearray([0x20] * length)
            elif type == 'BYTES': # 공백으로 초기화
                data = bytearray([0x20] * length)

        if length is None:
            if type == 'STRING':
                length = len(data)
            elif type == 'INT':
                length = 4
            elif type == 'SHORT':
                length = 2
            elif type == 'DOUBLE':
                length = 6


        if type == 'STRING':
            padded_string = str(data).rjust(length, pad)
            return padded_string.encode('utf-8')

        elif type == 'INT':
            return data.to_bytes(4, byteorder='big')

        elif type == 'SHORT':
            shortValue = data & 0xffff
            return shortValue.to_bytes(2, byteorder='big', signed=True)

        elif type == 'BYTE' or type == 'VARIABLE_LENGTH' or type == 'BYTES' or type == 'BASE64_DECMALS':
           return data

        elif type == 'DOUBLE':
            try:
                fval = float(data)
                return struct.pack('!d', fval)
            except ValueError:
                return struct.pack('!d', data)

    except Exception as e:
        logger.error(f'Utilitys encodeDataToBytes Exception : {data}:{type}:{length}  {e}')
        return None


def castingValue(data, type):
    try:
        logger.info()


    except Exception as e:
        logger.info(f'castingValue Exception :: {e}')


def requestGet(url, body, header=None):
    try:
        logger.info(f'requestGet url:{url} , header:{header} , body:{body}')
        if header is None:
            header = {
                "Content-Type": "application/json"
                # "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # 필요 시 추가
                # "User-Agent": "my-app/0.0.1",  # 필요 시 추가
                # "Accept": "application/json"  # 필요 시 추가
            }
        response = requests.get(url, headers=header, params=body)
        logger.info(f'requestGet Status Code::{response.status_code}')
        if response.headers.get('Content-Type') == 'application/json':
            json_response = response.json()
            return json_response
        else:
            return response.text
    except:
        logger.error(f'requestGet error: {traceback.format_exc()}')


def requestPost(url, body, header=None):
    try:
        logger.info(f'requestPost url:{url} , header:{header} , body:{body}')
        if header is None:
            header = {
                "Content-Type": "application/json"
                # "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # 필요 시 추가
                # "User-Agent": "my-app/0.0.1",  # 필요 시 추가
                # "Accept": "application/json"  # 필요 시 추가
            }
        response = requests.post(url, headers=header, json=body)
        logger.info(f'requestPost Status Code::{response.status_code}')

        if response.headers.get('Content-Type') == 'application/json':
            json_response = response.json()
            return json_response
        else:
            return response.text
    except:
        logger.error(f'requestPost error: {traceback.format_exc()}')
