


def selectSocketList(skId , useYn, pkgId='CORE'):

    query = []
    query.append('SELECT				 ')
    query.append('	A.PKG_ID             ')
    query.append('	, A.SK_ID            ')
    query.append('	, A.SK_GROUP         ')
    query.append('	, A.USE_YN           ')
    query.append('	, A.SK_CONN_TYPE     ')
    query.append('	, A.SK_TYPE          ')
    query.append('	, A.SK_CLIENT_TYPE   ')
    query.append('	, A.HD_ID            ')
    query.append('	, A.SK_PORT          ')
    query.append('	, A.SK_IP            ')
    query.append('	, A.SK_DELIMIT_TYPE  ')
    query.append('	, A.RELATION_VAL     ')
    query.append('	, A.SK_LOG           ')
    query.append('	, B.HD_TYPE          ')
    query.append('	, B.MSG_CLASS        ')
    query.append('	, B.MAX_LENGTH       ')
    query.append('	, B.MIN_LENGTH       ')
    query.append('FROM (                 ')
    query.append('	SELECT               ')
    query.append('		PKG_ID           ')
    query.append('		, SK_ID          ')
    query.append('		, SK_GROUP       ')
    query.append('		, USE_YN         ')
    query.append('		, SK_CONN_TYPE   ')
    query.append('		, SK_TYPE        ')
    query.append('		, SK_CLIENT_TYPE ')
    query.append('		, HD_ID          ')
    query.append('		, SK_PORT        ')
    query.append('		, SK_IP          ')
    query.append('		, SK_DELIMIT_TYPE')
    query.append('		, RELATION_VAL   ')
    query.append('		, SK_LOG         ')
    query.append('	FROM TB_SK_PKG_SK    ')
    query.append('WHERE 1=1    ')
    if(pkgId is not None):
        query.append(f'AND PKG_ID = "{pkgId}"')
    if(skId is not None):
        query.append(f'AND SK_ID = "{skId}"')
    if (useYn is not None):
        query.append(f'AND USE_YN = "{useYn}"')
    query.append(')A LEFT OUTER JOIN (   ')
    query.append('	SELECT               ')
    query.append('		HD_ID            ')
    query.append('		, HD_TYPE        ')
    query.append('		, MSG_CLASS      ')
    query.append('		, MAX_LENGTH     ')
    query.append('		, MIN_LENGTH     ')
    query.append('	FROM TB_SK_MSG_HD    ')
    query.append(')B                     ')
    query.append('ON A.HD_ID = B.HD_ID   ')

    return " ".join(query)

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
    query = []
    query.append('SELECT                 ')
    query.append('	MSG_ID               ')
    query.append('	, MSG_KEY_TYPE       ')
    query.append('	, MSG_KEY_VAL        ')
    query.append('	, MSG_DB_LOG_YN      ')
    query.append('	, MSG_DESC           ')
    query.append('	, MSG_KEY_VAL_DESC   ')
    query.append('	, MSG_KEY_LENGTH     ')
    query.append('	, MAX_WORK_SEC       ')
    query.append('FROM TB_SK_MSG_BODY    ')
    query.append('WHERE 1=1             ')
    query.append('ORDER BY MSG_KEY_VAL   ')

    return " ".join(query)


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

def selectSkInList(skId, pkgId):
    query = []
    query.append('SELECT                   ')
    query.append('	A.PKG_ID               ')
    query.append('	, A.SK_IN_SEQ          ')
    query.append('	, A.IN_SK_ID           ')
    query.append('	, A.IN_MSG_ID          ')
    query.append('	, B.MSG_KEY_TYPE       ')
    query.append('	, B.MSG_KEY_VAL        ')
    query.append('	, A.BZ_METHOD          ')
    query.append('	, A.IN_DESC            ')
    query.append('	, A.USE_YN             ')
    query.append('FROM (                   ')
    query.append('	SELECT                 ')
    query.append('		PKG_ID             ')
    query.append('		, SK_IN_SEQ        ')
    query.append('		, IN_SK_ID         ')
    query.append('		, IN_MSG_ID        ')
    query.append('		, BZ_METHOD        ')
    query.append('		, IN_DESC          ')
    query.append('		, USE_YN           ')
    query.append('	FROM TB_SK_PKG_SK_IN   ')
    query.append('	WHERE 1=1  ')
    if skId is not None and skId != '':
        query.append(f'	AND SK_ID = "{skId}"       ')
    if pkgId is not None and pkgId != '':
        query.append(f'	AND PKG_ID = "{pkgId}"       ')
    query.append('	AND USE_YN = "Y"       ')
    query.append(')A LEFT JOIN (             ')
    query.append('	SELECT                 ')
    query.append('		MSG_ID             ')
    query.append('		, MSG_KEY_TYPE     ')
    query.append('		, MSG_KEY_VAL      ')
    query.append('	FROM TB_SK_MSG_BODY    ')
    query.append(')B                         ')
    query.append('ON (A.IN_MSG_ID = B.MSG_ID)')

    return " ".join(query)

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


def selectSocketMSgList(msgId , mid):

    query = []
    query.append('SELECT              ')
    query.append('	MSG_ID            ')
    query.append('	,MSG_KEY_TYPE     ')
    query.append('	,MSG_KEY_VAL      ')
    query.append('	,MSG_DESC         ')
    query.append('from TB_SK_MSG_BODY A ')
    query.append('WHERE 1=1			   ')
    if msgId is not None and msgId != '':
        query.append(f'AND MSG_ID LIKE "%{msgId}%"  ')
    if mid is not None and mid != '':
        query.append(f'AND MSG_KEY_VAL LIKE "%{mid}%"  ')

    return " ".join(query)


def selectSocketMSgDtList(msgId ):

    query = []
    query.append('SELECT							')
    query.append('	B.MSG_DT_ORD                  ')
    query.append('	,B.MSG_DT_VAL_ID              ')
    query.append('	,B.MSG_DT_DESC                ')
    query.append('	,C.VAL_TYPE                   ')
    query.append('	,C.VAL_LEN                    ')
    query.append('from                            ')
    query.append('	TB_SK_MSG_BODY_DT B           ')
    query.append('	LEFT JOIN TB_SK_MSG_VAL C     ')
    query.append('	ON B.MSG_DT_VAL_ID = C.VAL_ID ')
    query.append('WHERE 1=1  ')
    if msgId is not None and msgId != '':
        query.append(f'AND B.MSG_ID = "{msgId}"  ')
    query.append('ORDER BY CAST(B.MSG_DT_ORD AS INTEGER) ASC;')
    return " ".join(query)


def saveSk(pkgId, skId, params):

    query = []
    query.append('UPDATE TB_SK_PKG_SK SET')
    for index, key in enumerate(params):
        if index == 0:
            query.append(f'"{key}" = "{params[key]}"')
        else:
            query.append(f',"{key}" = "{params[key]}"')
    query.append('WHERE 1=1')
    query.append(f'AND SK_ID = "{skId}"')
    query.append(f'AND PKG_ID = "{pkgId}"')

    result = " ".join(query)
    print(f'rs : {result}')
    return result


def insertSK(params):

    query = []
    keys = list(params.keys())
    values = [("" if str(v) is None else '""' if str(v) == "" else str(f"'{v}'")) for v in params.values()]


    query.append('INSERT INTO TB_SK_PKG_SK (')
    query.append(','.join(keys))
    query.append(') VALUES(')
    query.append(','.join(values))
    query.append(')')
    result = " ".join(query)
    print(f'rs : {result}')
    return result

def delSk(pkgId, skId):

    query = []
    query.append('DELETE FROM TB_SK_PKG_SK')
    query.append('WHERE 1=1')
    query.append(f'AND SK_ID = "{skId}"')
    query.append(f'AND PKG_ID = "{pkgId}"')


    result = " ".join(query)
    print(f'rs : {result}')
    return result
