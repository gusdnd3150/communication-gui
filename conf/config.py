import os
import json
from conf.logconfig import logger

defaultFoamt ={

        "HD_ID_LIST": [
            {
                "HD_ID": "H6",
                "DT_ORD": 1,
                "MSG_DT_ID": "TOTAL_LENGTH",
                "MSG_TY": "INT",
                "VAL_LEN": 4,
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "DT_ORD": 2,
                "MSG_DT_ID": "MSG_KEY_VAL",
                "MSG_TY": "BYTE",
                "VAL_LEN": 1,
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "DT_ORD": 3,
                "MSG_DT_ID": "DATA_TOTAL_LENGTH",
                "MSG_TY": "INT",
                "VAL_LEN": 4,
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "DT_ORD": 4,
                "MSG_DT_ID": "DATA_CNT",
                "MSG_TY": "SHORT",
                "VAL_LEN": 2,
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "DT_ORD": 5,
                "MSG_DT_ID": "REV",
                "MSG_TY": "BYTE",
                "VAL_LEN": 1,
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "DT_ORD": 6,
                "MSG_DT_ID": "SPARE",
                "MSG_TY": "BYTE",
                "VAL_LEN": 8,
                "VALUE": ""
            },
            {
                "HD_ID": "H4",
                "DT_ORD": 1,
                "MSG_DT_ID": "TOTAL_LENGTH",
                "MSG_TY": "BYTE",
                "VAL_LEN": 4,
                "VALUE": ""
            },
            {
                "HD_ID": "H4",
                "DT_ORD": 2,
                "MSG_DT_ID": "MSG_KEY_VAL",
                "MSG_TY": "BYTE",
                "VAL_LEN": 4,
                "VALUE": ""
            },
            {
                "HD_ID": "H4",
                "DT_ORD": 3,
                "MSG_DT_ID": "REV",
                "MSG_TY": "BYTE",
                "VAL_LEN": 3,
                "VALUE": ""
            },
            {
                "HD_ID": "H4",
                "DT_ORD": 4,
                "MSG_DT_ID": "SPARE",
                "MSG_TY": "BYTE",
                "VAL_LEN": 9,
                "VALUE": ""
            }
        ],
        "MSG_ID_LIST": [
            {
                "HD_ID": "H6",
                "MSG_ID": "ACK_MSG",
                "MSG_INT_VAL": 255,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "ACK_RESULT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "ACK_MSG",
                "MSG_INT_VAL": 255,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "ACK_MSG_ID",
                "VAL_LEN": 1,
                "MSG_TY": "BYTE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "ACK_MSG",
                "MSG_INT_VAL": 255,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "ACK_LENGTH",
                "VAL_LEN": 2,
                "MSG_TY": "SHORT",
                "VALUE": ""
            },
            {
                "HD_ID": "H4",
                "MSG_ID": "AC_CMMD_ACCEPT",
                "MSG_INT_VAL": 5,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "MID",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H4",
                "MSG_ID": "AC_ERROR",
                "MSG_INT_VAL": 4,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "MID",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H4",
                "MSG_ID": "AC_TIME_SEND",
                "MSG_INT_VAL": 82,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "DATE",
                "VAL_LEN": 19,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "BARCODE_SEND",
                "MSG_INT_VAL": 215,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "BARCODE_SEND",
                "MSG_INT_VAL": 215,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "MES_PROD_SEQ",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "BARCODE_SEND",
                "MSG_INT_VAL": 215,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "BARCODE_SND",
                "MSG_INT_VAL": 207,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "DEVICE_ID",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "BARCODE_SND",
                "MSG_INT_VAL": 207,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "BODY_NO",
                "MSG_INT_VAL": 128,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "BODY_NO",
                "MSG_INT_VAL": 128,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "BRING_CHANGE",
                "MSG_INT_VAL": 213,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "POS_ID",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "BRING_CHANGE",
                "MSG_INT_VAL": 213,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BRING_YN",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CMD_EXE",
                "MSG_INT_VAL": 69,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "SPAS_EXE",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CMD_EXE",
                "MSG_INT_VAL": 69,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "SPAS_CMD",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "COMM_ERROR",
                "MSG_INT_VAL": 162,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "COMM_ERROR",
                "MSG_INT_VAL": 162,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "POS_X",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "COMM_ERROR",
                "MSG_INT_VAL": 162,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "POS_Y",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "COMM_ERROR",
                "MSG_INT_VAL": 162,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "POS_Z",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CS_PROC_BARCODE",
                "MSG_INT_VAL": 126,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTRL_PROC_REQ",
                "MSG_INT_VAL": 139,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "CTRL_ID_3",
                "VAL_LEN": 3,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTRL_PROC_RES",
                "MSG_INT_VAL": 140,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "CTRL_ID",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTRL_PROC_RES",
                "MSG_INT_VAL": 140,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTRL_PROC_RES",
                "MSG_INT_VAL": 140,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTRL_PROC_RES",
                "MSG_INT_VAL": 140,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "LORA_CH",
                "VAL_LEN": 1,
                "MSG_TY": "BYTE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTRL_PROC_RES",
                "MSG_INT_VAL": 140,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTS_TAG_CAR_JOIN",
                "MSG_INT_VAL": 160,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTS_TAG_CAR_JOIN",
                "MSG_INT_VAL": 160,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTS_TAG_CAR_JOIN",
                "MSG_INT_VAL": 160,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "CTS_TAG_CAR_JOIN",
                "MSG_INT_VAL": 160,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "DEVICE_TYPE",
                "MSG_INT_VAL": 34,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "DEVICE_TYPE",
                "VAL_LEN": 2,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "DEVICE_TYPE",
                "MSG_INT_VAL": 34,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "DEVICE_TYPE",
                "VAL_LEN": 2,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "DROP_ARAM",
                "MSG_INT_VAL": 161,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "DROP_ARAM",
                "MSG_INT_VAL": 161,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "POS_X",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "DROP_ARAM",
                "MSG_INT_VAL": 161,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "POS_Y",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "DROP_ARAM",
                "MSG_INT_VAL": 161,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "POS_Z",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "FORY_BARCODE",
                "MSG_INT_VAL": 211,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "FORY_INOUT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "FORY_BARCODE",
                "MSG_INT_VAL": 211,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "FORY_EQUIP",
                "VAL_LEN": 11,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "FORY_BARCODE",
                "MSG_INT_VAL": 211,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "INTERLOCK_REQ",
                "MSG_INT_VAL": 206,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "INTERLOCK_REQ",
                "MSG_INT_VAL": 206,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "INTERLOCK_REQ",
                "MSG_INT_VAL": 206,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "ONE_ZERO",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "JOB_RESTART_REQ",
                "MSG_INT_VAL": 39,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "JOB_RESTART_REQ",
                "MSG_INT_VAL": 39,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_CANCEL",
                "MSG_INT_VAL": 123,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_CANCEL",
                "MSG_INT_VAL": 123,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_CANCEL",
                "MSG_INT_VAL": 123,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_FINISH",
                "MSG_INT_VAL": 124,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_FINISH",
                "MSG_INT_VAL": 124,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_FINISH",
                "MSG_INT_VAL": 124,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_FINISH",
                "MSG_INT_VAL": 124,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "TARGET_TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_SELECT",
                "MSG_INT_VAL": 122,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_SELECT",
                "MSG_INT_VAL": 122,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_SELECT",
                "MSG_INT_VAL": 122,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEPER_SELECT",
                "MSG_INT_VAL": 122,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "TARGET_TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_ALVE_REQ",
                "MSG_INT_VAL": 129,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "CTRL_ID",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_ALVE_REQ",
                "MSG_INT_VAL": 129,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "CTRL_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_ALVE_REQ",
                "MSG_INT_VAL": 129,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "UWB_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_ALVE_REQ",
                "MSG_INT_VAL": 129,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "MEM_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_ALVE_RES",
                "MSG_INT_VAL": 130,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "CTRL_ID",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_ALVE_RES",
                "MSG_INT_VAL": 130,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "CTRL_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_ALVE_RES",
                "MSG_INT_VAL": 130,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "UWB_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_ALVE_RES",
                "MSG_INT_VAL": 130,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "MEM_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_BODY_NO",
                "MSG_INT_VAL": 28,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_BODY_NO",
                "MSG_INT_VAL": 28,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_BODY_NO",
                "MSG_INT_VAL": 28,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_BODY_NO",
                "MSG_INT_VAL": 28,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KEEP_BODY_NO",
                "MSG_INT_VAL": 28,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "TARGET_TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "KMI_DEL_BODY_NO",
                "MSG_INT_VAL": 181,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LAMP_SEND_DATA",
                "MSG_INT_VAL": 214,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LAMP_SEND_DATA",
                "MSG_INT_VAL": 214,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "DP_CMT_S",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LAMP_SEND_DATA",
                "MSG_INT_VAL": 214,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "OPTION_RESERVE",
                "VAL_LEN": 5,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LAMP_SEND_DATA",
                "MSG_INT_VAL": 214,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "SEND_TY",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LINE_BODY_NO_RES",
                "MSG_INT_VAL": 202,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LINE_BODY_NO_RES",
                "MSG_INT_VAL": 202,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LINE_BODY_NO_RES",
                "MSG_INT_VAL": 202,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "ONE_ZERO",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LINE_RUN_STATUS",
                "MSG_INT_VAL": 204,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LINE_RUN_STATUS",
                "MSG_INT_VAL": 204,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "ONE_ZERO",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LINE_SPEED",
                "MSG_INT_VAL": 205,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LINE_SPEED",
                "MSG_INT_VAL": 205,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "LINE_SPD",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO",
                "MSG_INT_VAL": 193,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO",
                "MSG_INT_VAL": 193,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "POS_X",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO",
                "MSG_INT_VAL": 193,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "POS_Y",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO",
                "MSG_INT_VAL": 193,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "POS_Z",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO",
                "MSG_INT_VAL": 193,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "OCCR_DTMS",
                "VAL_LEN": 18,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "POS_ID",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "POS_X",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "POS_Y",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 7,
                "MSG_DT_ID": "POS_Z",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 8,
                "MSG_DT_ID": "ANGL",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 9,
                "MSG_DT_ID": "CAR_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO2",
                "MSG_INT_VAL": 199,
                "MSG_DT_ORD": 10,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO3",
                "MSG_INT_VAL": 210,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO3",
                "MSG_INT_VAL": 210,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "POS_X",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO3",
                "MSG_INT_VAL": 210,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "POS_Y",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO3",
                "MSG_INT_VAL": 210,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "POS_Z",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LOC_INFO3",
                "MSG_INT_VAL": 210,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "OCCR_DTMS",
                "VAL_LEN": 18,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_DOOR_SUB",
                "MSG_INT_VAL": 145,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_DOOR_SUB",
                "MSG_INT_VAL": 145,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_DOOR_SUB",
                "MSG_INT_VAL": 145,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LIQ_REQ",
                "VAL_LEN": 2,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "LIQ_DEVICE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "LIQ_DEVICE_NO",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "LIQ_BODY_NO",
                "VAL_LEN": 12,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "LIQ_TEMP1",
                "VAL_LEN": 8,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "LIQ_TEMP2",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 7,
                "MSG_DT_ID": "LIQ_TEMP3",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 8,
                "MSG_DT_ID": "LIQ_TOTAL_RSLT",
                "VAL_LEN": 2,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 9,
                "MSG_DT_ID": "LIQ_L_CHK_RSLT",
                "VAL_LEN": 2,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 10,
                "MSG_DT_ID": "LIQ_L_CHK",
                "VAL_LEN": 4,
                "MSG_TY": "FLOAT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 11,
                "MSG_DT_ID": "LIQ_S_CHK_RSLT",
                "VAL_LEN": 2,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 12,
                "MSG_DT_ID": "LIQ_S_CHK",
                "VAL_LEN": 4,
                "MSG_TY": "FLOAT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 13,
                "MSG_DT_ID": "LIQ_ABS_RSLT",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 14,
                "MSG_DT_ID": "LIQ_SECOND_VAC",
                "VAL_LEN": 4,
                "MSG_TY": "FLOAT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 15,
                "MSG_DT_ID": "LIQ_INJE_RELS",
                "VAL_LEN": 2,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 16,
                "MSG_DT_ID": "LIQ_INJE_PRESS",
                "VAL_LEN": 4,
                "MSG_TY": "FLOAT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 17,
                "MSG_DT_ID": "LIQ_TEMP4",
                "VAL_LEN": 2,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 18,
                "MSG_DT_ID": "LIQ_INJE_MASS",
                "VAL_LEN": 4,
                "MSG_TY": "FLOAT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 19,
                "MSG_DT_ID": "LIQ_DENSITY",
                "VAL_LEN": 2,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "LP_LIQUID_RSLT",
                "MSG_INT_VAL": 192,
                "MSG_DT_ORD": 20,
                "MSG_DT_ID": "LIQ_TEMP5",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_CTS_CHECK",
                "MSG_INT_VAL": 212,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_CTS_CHECK",
                "MSG_INT_VAL": 212,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_CTS_CHECK",
                "MSG_INT_VAL": 212,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "MES_PROD_SEQ",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_CTS_CHECK",
                "MSG_INT_VAL": 212,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_CTS_CHECK",
                "MSG_INT_VAL": 212,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_PROC_IN",
                "MSG_INT_VAL": 165,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "POS_ID",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_PROC_IN",
                "MSG_INT_VAL": 165,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "ACTION",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_PROC_IN",
                "MSG_INT_VAL": 165,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_PROC_IN",
                "MSG_INT_VAL": 165,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_PROC_IN",
                "MSG_INT_VAL": 165,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_PROC_IN",
                "MSG_INT_VAL": 165,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_PROD_INFO",
                "MSG_INT_VAL": 144,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "DP_CMT_S",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_PROD_INFO",
                "MSG_INT_VAL": 144,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "MES_PROD_INFO",
                "MSG_INT_VAL": 144,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "NEXT_BODY_NO",
                "MSG_INT_VAL": 178,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "NEXT_BODY_NO",
                "MSG_INT_VAL": 178,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PASS_BODY_REQ",
                "MSG_INT_VAL": 127,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PASS_BODY_REQ",
                "MSG_INT_VAL": 127,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PASS_POINT_REQ",
                "MSG_INT_VAL": 125,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PASS_POINT_REQ",
                "MSG_INT_VAL": 125,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_IN",
                "MSG_INT_VAL": 132,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "POS_ID",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_IN",
                "MSG_INT_VAL": 132,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_IN",
                "MSG_INT_VAL": 132,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_IN",
                "MSG_INT_VAL": 132,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_IN",
                "MSG_INT_VAL": 132,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_IN",
                "MSG_INT_VAL": 132,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT",
                "MSG_INT_VAL": 133,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "POS_ID",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT",
                "MSG_INT_VAL": 133,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT",
                "MSG_INT_VAL": 133,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT",
                "MSG_INT_VAL": 133,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT",
                "MSG_INT_VAL": 133,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT",
                "MSG_INT_VAL": 133,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT_VCC",
                "MSG_INT_VAL": 77,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "POS_ID",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT_VCC",
                "MSG_INT_VAL": 77,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT_VCC",
                "MSG_INT_VAL": 77,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT_VCC",
                "MSG_INT_VAL": 77,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT_VCC",
                "MSG_INT_VAL": 77,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_OUT_VCC",
                "MSG_INT_VAL": 77,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_RSLT",
                "MSG_INT_VAL": 142,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "ACTION",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_RSLT",
                "MSG_INT_VAL": 142,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_RSLT",
                "MSG_INT_VAL": 142,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_RSLT",
                "MSG_INT_VAL": 142,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_RSLT",
                "MSG_INT_VAL": 142,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_RSLT",
                "MSG_INT_VAL": 142,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PROC_RSLT",
                "MSG_INT_VAL": 142,
                "MSG_DT_ORD": 7,
                "MSG_DT_ID": "RESERVE",
                "VAL_LEN": 128,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PT_BODY_NO_RES",
                "MSG_INT_VAL": 201,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PT_BODY_NO_RES",
                "MSG_INT_VAL": 201,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "ONE_ZERO",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PT_BODY_NO_RES",
                "MSG_INT_VAL": 201,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "PT_BODY_NO_RES",
                "MSG_INT_VAL": 201,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "BODY_NO_SUB",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SELECT_BODY_REQ",
                "MSG_INT_VAL": 50,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SELECT_BODY_REQ",
                "MSG_INT_VAL": 50,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SELECT_BODY_REQ",
                "MSG_INT_VAL": 50,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H4",
                "MSG_ID": "SEND_BODY_NO",
                "MSG_INT_VAL": 50,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "VIN_NO",
                "VAL_LEN": 25,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H4",
                "MSG_ID": "SEND_JOB_NO",
                "MSG_INT_VAL": 38,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "JOB_ID",
                "VAL_LEN": 3,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SENS_LIST",
                "MSG_INT_VAL": 197,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SENS_LIST",
                "MSG_INT_VAL": 197,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "IP",
                "VAL_LEN": 15,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SENS_LIST",
                "MSG_INT_VAL": 197,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "Y_N",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SENS_LIST",
                "MSG_INT_VAL": 197,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SENS_LIST",
                "MSG_INT_VAL": 197,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SEWIO_LOC_INFO",
                "MSG_INT_VAL": 191,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "SEWIO_JSON",
                "VAL_LEN": 2500,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SIGN_OFF_IN",
                "MSG_INT_VAL": 138,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SIGN_OFF_IN",
                "MSG_INT_VAL": 138,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "RESULT_INT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SIMUL_NEW_CAR",
                "MSG_INT_VAL": 168,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SIMUL_NEW_CAR",
                "MSG_INT_VAL": 168,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "SIMUL_NEW_CAR",
                "MSG_INT_VAL": 168,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "STD_INFO",
                "MSG_INT_VAL": 134,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "STD_INFO",
                "MSG_INT_VAL": 134,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "STD_INFO",
                "MSG_INT_VAL": 134,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "CTRL_ID",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_PROC_IN",
                "MSG_INT_VAL": 194,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_PROC_IN",
                "MSG_INT_VAL": 194,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_PROC_IN",
                "MSG_INT_VAL": 194,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_STAT",
                "MSG_INT_VAL": 131,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_STAT",
                "MSG_INT_VAL": 131,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "MCU_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_STAT",
                "MSG_INT_VAL": 131,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "GYRO_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_STAT",
                "MSG_INT_VAL": 131,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "DATA_UWB_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_STAT",
                "MSG_INT_VAL": 131,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "POS_UWB_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_STAT",
                "MSG_INT_VAL": 131,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "MEM_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_STAT",
                "MSG_INT_VAL": 131,
                "MSG_DT_ORD": 7,
                "MSG_DT_ID": "BAT_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TAG_STAT",
                "MSG_INT_VAL": 131,
                "MSG_DT_ORD": 8,
                "MSG_DT_ID": "DATA_STAT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TERM_BODY_NO",
                "MSG_INT_VAL": 176,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TERM_BODY_NO",
                "MSG_INT_VAL": 176,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TIRE_SEND_DATA",
                "MSG_INT_VAL": 216,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TIRE_SEND_DATA",
                "MSG_INT_VAL": 216,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "DP_CMT_S",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TIRE_SEND_DATA",
                "MSG_INT_VAL": 216,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "OPTION_RESERVE",
                "VAL_LEN": 5,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TIRE_SEND_DATA",
                "MSG_INT_VAL": 216,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "SEND_TY",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_CAR_IN",
                "MSG_INT_VAL": 203,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_CAR_IN",
                "MSG_INT_VAL": 203,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_CAR_IN",
                "MSG_INT_VAL": 203,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_IN",
                "MSG_INT_VAL": 146,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "POS_ID",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_IN",
                "MSG_INT_VAL": 146,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_IN",
                "MSG_INT_VAL": 146,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "TOOL_TAG_ID",
                "VAL_LEN": 15,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_IN",
                "MSG_INT_VAL": 146,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_IN",
                "MSG_INT_VAL": 146,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "WKSP_SEQ",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_IN",
                "MSG_INT_VAL": 146,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_IN",
                "MSG_INT_VAL": 146,
                "MSG_DT_ORD": 7,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_OUT",
                "MSG_INT_VAL": 147,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "POS_ID",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_OUT",
                "MSG_INT_VAL": 147,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_OUT",
                "MSG_INT_VAL": 147,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "TOOL_TAG_ID",
                "VAL_LEN": 15,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_OUT",
                "MSG_INT_VAL": 147,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_OUT",
                "MSG_INT_VAL": 147,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "WKSP_SEQ",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_OUT",
                "MSG_INT_VAL": 147,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TOOL_OUT",
                "MSG_INT_VAL": 147,
                "MSG_DT_ORD": 7,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TPMS_BARCODE_SCAN",
                "MSG_INT_VAL": 136,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "DEVICE_ID",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TPMS_BARCODE_SCAN",
                "MSG_INT_VAL": 136,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TPMS_BODY_NO",
                "MSG_INT_VAL": 141,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "DP_CMT_S",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "TPMS_BODY_NO",
                "MSG_INT_VAL": 141,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "T_APP_BODY_NO",
                "MSG_INT_VAL": 29,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "T_APP_BODY_NO",
                "MSG_INT_VAL": 29,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "T_APP_BODY_NO",
                "MSG_INT_VAL": 29,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "TOOL_ID",
                "VAL_LEN": 6,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "T_APP_BODY_NO",
                "MSG_INT_VAL": 29,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "OCCR_DTM",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "T_APP_BODY_NO",
                "MSG_INT_VAL": 29,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "CS_TYPE",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_DEL_BODY_NO",
                "MSG_INT_VAL": 180,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_LINES_BODY_NOS",
                "MSG_INT_VAL": 177,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_LINES_BODY_NOS",
                "MSG_INT_VAL": 177,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "MES_PROD_SEQ",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_LINES_BODY_NOS",
                "MSG_INT_VAL": 177,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_LINES_BODY_NOS",
                "MSG_INT_VAL": 177,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR",
                "MSG_INT_VAL": 170,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR",
                "MSG_INT_VAL": 170,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR",
                "MSG_INT_VAL": 170,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "MES_PROD_SEQ",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR",
                "MSG_INT_VAL": 170,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR",
                "MSG_INT_VAL": 170,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "MAPPING_FLAG",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR_PROC",
                "MSG_INT_VAL": 169,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR_PROC",
                "MSG_INT_VAL": 169,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR_PROC",
                "MSG_INT_VAL": 169,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "MES_PROD_SEQ",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR_PROC",
                "MSG_INT_VAL": 169,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "PROC_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR_PROC",
                "MSG_INT_VAL": 169,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "MAPPING_FLAG",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_CAR_PROC",
                "MSG_INT_VAL": 169,
                "MSG_DT_ORD": 6,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_TERM_CAR",
                "MSG_INT_VAL": 175,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_TERM_CAR",
                "MSG_INT_VAL": 175,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEW_TERM_CAR",
                "MSG_INT_VAL": 175,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "DP_CMT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEXT_BODY_NO",
                "MSG_INT_VAL": 179,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEXT_BODY_NO",
                "MSG_INT_VAL": 179,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "BODY_NO",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEXT_BODY_NO",
                "MSG_INT_VAL": 179,
                "MSG_DT_ORD": 3,
                "MSG_DT_ID": "BODY_NO_SUB",
                "VAL_LEN": 10,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEXT_BODY_NO",
                "MSG_INT_VAL": 179,
                "MSG_DT_ORD": 4,
                "MSG_DT_ID": "DP_CMT",
                "VAL_LEN": 4,
                "MSG_TY": "INT",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NEXT_BODY_NO",
                "MSG_INT_VAL": 179,
                "MSG_DT_ORD": 5,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NVERTER_RPM",
                "MSG_INT_VAL": 172,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_NVERTER_RPM",
                "MSG_INT_VAL": 172,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "LINE_SPD",
                "VAL_LEN": 8,
                "MSG_TY": "DOUBLE",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_PLANT_ACTION",
                "MSG_INT_VAL": 173,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "LINE_CD",
                "VAL_LEN": 4,
                "MSG_TY": "STRING",
                "VALUE": ""
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "VCC_PLANT_ACTION",
                "MSG_INT_VAL": 173,
                "MSG_DT_ORD": 2,
                "MSG_DT_ID": "ONE_ZERO",
                "VAL_LEN": 1,
                "MSG_TY": "STRING",
                "VALUE": "1"
            },
            {
                "HD_ID": "H6",
                "MSG_ID": "WARNING_LIGHT",
                "MSG_INT_VAL": 148,
                "MSG_DT_ORD": 1,
                "MSG_DT_ID": "TAG_ID",
                "VAL_LEN": 14,
                "MSG_TY": "STRING",
                "VALUE": ""
            }
        ],
        "SAVE_LIST":[
                    # {
                    #     "ALIAS":"",
                    #     "MSG" : ""
                    # }
        ],

        "DB_INFO":{
            "TYPE":"Tibero",
            "DB_IP":"dev.teia.co.kr",
            "DB_PORT":8629,
            "DB_SID":"tibero",
            "USER":"HMMI_SDOP",
            "PASSWORD":"HMMI_SDOP",
            "SELECT_HD_QUERY":"",
            "SELECT_MSG_QUERY":""
        }

}


# 파일 경로
file_path = "./config.json"

# 파일이 없을 경우에만 JSON 파일 생성
if not os.path.exists(file_path):
    with open(file_path, "w") as file:
        json.dump(defaultFoamt, file)
        print(f"{file_path} 파일이 생성되었습니다.")
        logger.info("defualt config file created")
else:
    logger.info("defualt config file is already exits")
