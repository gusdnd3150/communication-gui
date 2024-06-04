


def selectSocketList():
    string = 'SELECT					 '\
                '	A.PKG_ID             '\
                '	, A.SK_ID            '\
                '	, A.SK_GROUP         '\
                '	, A.USE_YN           '\
                '	, A.SK_CONN_TYPE     '\
                '	, A.SK_TYPE          '\
                '	, A.SK_CLIENT_TYPE   '\
                '	, A.HD_ID            '\
                '	, A.SK_PORT          '\
                '	, A.SK_IP            '\
                '	, A.SK_DELIMIT_TYPE  '\
                '	, A.RELATION_VAL     '\
                '	, A.SK_LOG           '\
                '	, B.HD_TYPE          '\
                '	, B.MSG_CLASS        '\
                '	, B.MAX_LENGTH       '\
                '	, B.MIN_LENGTH       '\
                'FROM (                   '\
                '	SELECT               '\
                '		PKG_ID           '\
                '		, SK_ID          '\
                '		, SK_GROUP       '\
                '		, USE_YN         '\
                '		, SK_CONN_TYPE   '\
                '		, SK_TYPE        '\
                '		, SK_CLIENT_TYPE '\
                '		, HD_ID          '\
                '		, SK_PORT        '\
                '		, SK_IP          '\
                '		, SK_DELIMIT_TYPE'\
                '		, RELATION_VAL   '\
                '		, SK_LOG         '\
                '	FROM TB_SK_PKG_SK    '\
                '	WHERE PKG_ID = "CORE"    '\
                '	AND USE_YN = "Y"     '\
                ')A LEFT OUTER JOIN (     '\
                '	SELECT               '\
                '		HD_ID            '\
                '		, HD_TYPE        '\
                '		, MSG_CLASS      '\
                '		, MAX_LENGTH     '\
                '		, MIN_LENGTH     '\
                '	FROM TB_SK_MSG_HD    '\
                ')B                       '\
                'ON A.HD_ID = B.HD_ID     '\

    return string

def selectTbSkMsgHdDt():
    return 'SELECT                  '\
            '	HD_ID               '\
            '	, DT_ORD            '\
            '	, DT_ID             '\
            '	, DT_TYPE           '\
            '	, DT_LEN            '\
            '	, DT_NAME           '\
            '	, DT_DESC           '\
            '	, MSG_LEN_REL_YN    '\
            '	, MSG_ID_REL_YN     '\
            '	, DEFAULT_VALUE     '\
            'FROM TB_SK_MSG_HD_DT    '\
            'WHERE HD_ID = "{}"  '\
            'ORDER BY DT_ORD		'\

def selectHdLen():
    return 'SELECT                       '\
            '	HD_ID                    '\
            '	, SUM(DT_LEN) AS HD_LEN  '\
            'FROM TB_SK_MSG_HD_DT         '\
            'WHERE HD_ID = "{}"      '\
            'GROUP BY HD_ID			 '


def selectMsgBodyList():
    return 'SELECT             '\
        '	MSG_ID             '\
        '	, MSG_KEY_TYPE     '\
        '	, MSG_KEY_VAL      '\
        '	, MSG_DB_LOG_YN    '\
        '	, MSG_DESC         '\
        '	, MSG_KEY_VAL_DESC '\
        '	, MSG_KEY_LENGTH   '\
        '	, MAX_WORK_SEC     '\
        'FROM TB_SK_MSG_BODY    '\
        'ORDER BY MSG_KEY_VAL   '


def selectTbSkMsgBodyDtAndVal():
    return 'SELECT                            '\
        '	A.MSG_ID                      '\
        '	, A.MSG_DT_ORD                '\
        '	, A.MSG_DT_DESC               '\
        '	, B.VAL_ID                    '\
        '	, B.VAL_TYPE                  '\
        '	, B.VAL_LEN                   '\
        '	, B.VAL_DESC                  '\
        'FROM (                            '\
        '	SELECT                        '\
        '		MSG_ID                    '\
        '		, MSG_DT_ORD              '\
        '		, MSG_DT_VAL_ID           '\
        '		, MSG_DT_DESC             '\
        '	FROM TB_SK_MSG_BODY_DT        '\
        '	WHERE MSG_ID = "{}"           '\
        ')A, (                             '\
        '	SELECT                        '\
        '		VAL_ID                    '\
        '		, VAL_TYPE                '\
        '		, VAL_LEN                 '\
        '		, VAL_DESC                '\
        '	FROM TB_SK_MSG_VAL            '\
        ')B                                '\
        'WHERE A.MSG_DT_VAL_ID = B.VAL_ID  '\
        'ORDER BY MSG_ID, MSG_DT_ORD		'\

def selectMsgLen():
    return 'SELECT                           '\
        '	A.MSG_ID                     '\
        '	, SUM(VAL_LEN) AS MSG_LEN    '\
        'FROM (                           '\
        '	SELECT                       '\
        '		MSG_ID                   '\
        '		, MSG_DT_ORD             '\
        '		, MSG_DT_VAL_ID          '\
        '		, MSG_DT_DESC            '\
        '	FROM TB_SK_MSG_BODY_DT       '\
        '	WHERE MSG_ID = "{}"     '\
        ')A, (                            '\
        '	SELECT                       '\
        '		VAL_ID                   '\
        '		, VAL_TYPE               '\
        '		, VAL_LEN                '\
        '		, VAL_DESC               '\
        '	FROM TB_SK_MSG_VAL           '\
        ')B                               '\
        'WHERE A.MSG_DT_VAL_ID = B.VAL_ID '\
        'GROUP BY A.MSG_ID				 '\

def selectSkInList():
    return 'SELECT                     '\
            '	A.PKG_ID               '\
            '	, A.SK_IN_SEQ          '\
            '	, A.IN_SK_ID           '\
            '	, A.IN_MSG_ID          '\
            '	, B.MSG_KEY_TYPE       '\
            '	, B.MSG_KEY_VAL        '\
            '	, A.BZ_METHOD          '\
            '	, A.IN_DESC            '\
            '	, A.USE_YN             '\
            'FROM (                     '\
            '	SELECT                 '\
            '		PKG_ID             '\
            '		, SK_IN_SEQ        '\
            '		, IN_SK_ID         '\
            '		, IN_MSG_ID        '\
            '		, BZ_METHOD        '\
            '		, IN_DESC          '\
            '		, USE_YN           '\
            '	FROM TB_SK_PKG_SK_IN   '\
            '	WHERE PKG_ID = "CORE"  '\
            '	AND USE_YN = "Y"       '\
            ')A LEFT JOIN (             '\
            '	SELECT                 '\
            '		MSG_ID             '\
            '		, MSG_KEY_TYPE     '\
            '		, MSG_KEY_VAL      '\
            '	FROM TB_SK_MSG_BODY    '\
            ')B                         '\
            'ON (A.IN_MSG_ID = B.MSG_ID)'


def selectSkOutList():
    return 'SELECT                   '\
            '	PKG_ID               '\
            '	, SK_OUT_SEQ         '\
            '	, OUT_SK_ID          '\
            '	, OUT_MSG_ID         '\
            '	, OUT_DESC           '\
            '	, USE_YN             '\
            'FROM TB_SK_PKG_SK_OUT    '\
            'WHERE PKG_ID = "CORE" '\
            'AND USE_YN = "Y"		 '

def selectListTbSkSch():
    return 'SELECT                '\
            '	PKG_ID            '\
            '	, SCH_ID          '\
            '	, BZ_METHOD       '\
            '	, SCH_DESC        '\
            '	, USE_YN          '\
            '	, SCH_JOB         '\
            '	, SCH_JOB_TYPE    '\
            'FROM TB_SK_PKG_SCH    '\
            'WHERE PKG_ID = "CORE" '\
            'AND USE_YN = "Y"      '

def selectListTbSkBz ():
    return 'SELECT            '  \
            '	PKG_ID            '  \
            '	, SK_GROUP        '  \
            '	, BZ_TYPE         '  \
            '	, USE_YN          '  \
            '	, BZ_METHOD       '  \
            '	, SEC             '  \
            '	, BZ_DESC         '  \
            'FROM TB_SK_PKG_SK_BZ  '  \
            'WHERE PKG_ID = "CORE" ' \
            'AND SK_GROUP = "{}"	' \
            'AND USE_YN = "Y"	'