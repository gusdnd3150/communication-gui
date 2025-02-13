

def selectPkgCombo():
    query = []
    query.append('SELECT PKG_ID    ')
    query.append('from TB_SK_PKG_SK')
    query.append('group by PKG_ID  ')
    return " ".join(query)


def selectPlcAddrList(pkgId, plcId):
    query = []
    query.append('SELECT             ')
    query.append(' PKG_ID    ')
    query.append(',PLC_ID   ')
    query.append(',ADDR     ')
    query.append(',POS      ')
    query.append(',LENGTH   ')
    query.append(',USE_YN   ')
    query.append(',ADDR_DESC')
    query.append('FROM TB_SK_PKG_PLC_ADDR ')
    query.append('WHERE 1=1 ')
    query.append(f'AND USE_YN = "Y" ')
    if (pkgId is not None):
        query.append(f'AND PKG_ID = "{pkgId}"')
    if (plcId is not None):
        query.append(f'AND PLC_ID = "{plcId}"')

    return " ".join(query)


def selectPlcList(skId , useYn, pkgId='CORE'):

    query = []
    query.append('SELECT             ')
    query.append(' PKG_ID         ')
    query.append(' ,PLC_ID         ')
    query.append(' ,USE_YN         ')
    query.append(' ,PLC_MAKER      ')
    query.append(' ,PLC_PTOROTOCOL ')
    query.append(' ,SLOT           ')
    query.append(' ,PLC_PORT       ')
    query.append(' ,PLC_IP         ')
    query.append(' ,BASE_SK_IP     ')
    query.append(' ,BASE_SK_PORT   ')
    query.append(' ,PLC_DESC       ')
    query.append(' ,SK_LOG         ')
    query.append(' ,COMM_TY        ')
    query.append(' ,CPU_TY        ')
    query.append('FROM TB_SK_PKG_PLC ')
    query.append('WHERE 1=1 ')
    if (pkgId is not None):
        query.append(f'AND PKG_ID = "{pkgId}"')
    if (skId is not None):
        query.append(f'AND PLC_ID = "{skId}"')
    if (useYn is not None):
        query.append(f'AND USE_YN = "{useYn}"')

    return " ".join(query)


def selectInitSocketList(skId , useYn, pkgId='CORE'):

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
    if(pkgId is not None and pkgId != ''):
        query.append(f'AND PKG_ID = "{pkgId}"')
    if(skId is not None and skId != ''):
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
    query.append('ORDER BY PKG_ID , SK_CONN_TYPE, SK_ID')

    return " ".join(query)

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
    if(pkgId is not None and pkgId != ''):
        query.append(f'AND PKG_ID LIKE "%{pkgId}%"')
    if(skId is not None and skId != ''):
        query.append(f'AND SK_ID LIKE "%{skId}%"')
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
    query.append('ORDER BY PKG_ID , SK_CONN_TYPE, SK_ID')

    return " ".join(query)

def selectSocketInList(skId , useYn, pkgId='CORE'):

    query = []
    query.append('SELECT 			   ')
    query.append('	PKG_ID             ')
    query.append('	,SK_IN_SEQ         ')
    query.append('	,IN_SK_ID          ')
    query.append('	,IN_MSG_ID         ')
    query.append('	,BZ_METHOD         ')
    query.append('	,IN_DESC           ')
    query.append('	,USE_YN            ')
    query.append('	,REG_ID            ')
    query.append('	,UPD_ID            ')
    query.append('FROM TB_SK_PKG_SK_IN ')
    query.append('WHERE 1=1            ')
    if(pkgId is not None and pkgId != ''):
        query.append(f'AND PKG_ID like "%{pkgId}%"')
    if(skId is not None and skId != ''):
        query.append(f'AND IN_SK_ID like "%{skId}%"')
    if (useYn is not None):
        query.append(f'AND USE_YN = "{useYn}"')
    query.append(' ORDER BY PKG_ID, SK_IN_SEQ ')


    return " ".join(query)

def selectHeaderList():

    query = []
    query.append('SELECT 			   ')
    query.append('	PKG_ID             ')
    query.append('	,SK_IN_SEQ         ')
    query.append('	,IN_SK_ID          ')
    query.append('	,IN_MSG_ID         ')
    query.append('	,BZ_METHOD         ')
    query.append('	,IN_DESC           ')
    query.append('	,USE_YN            ')
    query.append('	,REG_ID            ')
    query.append('	,UPD_ID            ')
    query.append('FROM TB_SK_PKG_SK_IN ')
    query.append('WHERE 1=1            ')
    query.append(' ORDER BY PKG_ID, SK_IN_SEQ ')
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
        'ORDER BY MSG_ID, CAST(MSG_DT_ORD AS INTEGER)'\

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
    query.append('ORDER BY A.PKG_ID, A.SK_IN_SEQ')

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

def selectListTbSkSch(pkgId='CORE'):
    query =[]
    query.append('SELECT                 ')
    query.append('	PKG_ID               ')
    query.append('	, SCH_ID             ')
    query.append('	, BZ_METHOD          ')
    query.append('	, SCH_DESC           ')
    query.append('	, USE_YN             ')
    query.append('	, SCH_JOB            ')
    query.append('	, SCH_JOB_TYPE       ')
    query.append('FROM TB_SK_PKG_SCH     ')
    query.append('WHERE 1=1')
    if(pkgId is not None):
        query.append(f'AND PKG_ID = "{pkgId}" ')
    query.append('AND USE_YN = "Y"       ')
    return " ".join(query)

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
            'WHERE 1=1 ' \
            'AND SK_GROUP = "{}"	' \
            'AND USE_YN = "Y"	'


def selectSocketMSgList(msgId , mid):

    query = []
    query.append('SELECT              ')
    query.append('	MSG_ID            ')
    query.append('	,MSG_KEY_TYPE     ')
    query.append('	,MSG_KEY_VAL      ')
    query.append('	,MSG_DESC         ')
    query.append('	,MSG_KEY_LENGTH         ')
    query.append('from TB_SK_MSG_BODY A ')
    query.append('WHERE 1=1			   ')
    if msgId is not None and msgId != '':
        query.append(f'AND (MSG_ID LIKE "%{msgId}%" or MSG_DESC LIKE "%{msgId}%"  )')
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
    query.append('	,C.VAL_DESC                    ')
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



def insertIn(params):

    query = []
    keys = list(params.keys())
    values = [("" if str(v) is None else '""' if str(v) == "" else str(f"'{v}'")) for v in params.values()]
    query.append('INSERT INTO TB_SK_PKG_SK_IN (')
    query.append(','.join(keys))
    query.append(') VALUES(')
    query.append(','.join(values))
    query.append(')')
    result = " ".join(query)
    print(f'rs : {result}')
    return result

def saveIn(pkgId,skId,  inseq, params):

    query = []
    query.append('UPDATE TB_SK_PKG_SK_IN SET')
    for index, key in enumerate(params):
        if index == 0:
            query.append(f'"{key}" = "{params[key]}"')
        else:
            query.append(f',"{key}" = "{params[key]}"')
    query.append('WHERE 1=1')
    query.append(f'AND SK_IN_SEQ = "{inseq}"')
    query.append(f'AND PKG_ID = "{pkgId}"')
    query.append(f'AND IN_SK_ID = "{skId}"')

    result = " ".join(query)
    print(f'rs : {result}')
    return result



def delIn(pkgId, inseq):

    query = []
    query.append('DELETE FROM TB_SK_PKG_SK_IN')
    query.append('WHERE 1=1')
    query.append(f'AND SK_IN_SEQ = "{inseq}"')
    query.append(f'AND PKG_ID = "{pkgId}"')

    result = " ".join(query)
    print(f'rs : {result}')
    return result


def selectBzList(skGroupId , useYn, pkgId='CORE'):

    query = []
    query.append('SELECT               ')
    query.append('	PKG_ID             ')
    query.append('	,SK_GROUP          ')
    query.append('	,BZ_TYPE           ')
    query.append('	,USE_YN            ')
    query.append('	,BZ_METHOD         ')
    query.append('	,SEC               ')
    query.append('	,BZ_DESC           ')
    query.append('FROM TB_SK_PKG_SK_BZ ')
    query.append('WHERE 1=1 ')
    if(pkgId is not None):
        query.append(f'AND PKG_ID = "{pkgId}"')
    if(skGroupId is not None):
        query.append(f'AND SK_GROUP = "{skGroupId}"')
    if (useYn is not None):
        query.append(f'AND USE_YN = "{useYn}"')

    return " ".join(query)

def insertTable(params,tableNm):

    query = []
    keys = list(params.keys())
    values = [("" if str(v) is None else '""' if str(v) == "" else str(f"'{v}'")) for v in params.values()]
    query.append(f'INSERT INTO {tableNm} (')
    query.append(','.join(keys))
    query.append(') VALUES(')
    query.append(','.join(values))
    query.append(')')
    result = " ".join(query)
    print(f'rs : {result}')
    return result

def saveBz(pkgId, skGroup,bzTy, params):

    query = []
    query.append('UPDATE TB_SK_PKG_SK_BZ SET')
    for index, key in enumerate(params):
        if index == 0:
            query.append(f'"{key}" = "{params[key]}"')
        else:
            query.append(f',"{key}" = "{params[key]}"')
    query.append('WHERE 1=1')
    query.append(f'AND PKG_ID = "{pkgId}"')
    query.append(f'AND SK_GROUP = "{skGroup}"')
    query.append(f'AND BZ_TYPE = "{bzTy}"')

    result = " ".join(query)
    print(f'rs : {result}')
    return result

def delBz(pkgId, skgroup, bzty):

    query = []
    query.append('DELETE FROM TB_SK_PKG_SK_BZ')
    query.append('WHERE 1=1')
    query.append(f'AND PKG_ID = "{pkgId}"')
    query.append(f'AND SK_GROUP = "{skgroup}"')
    query.append(f'AND BZ_TYPE = "{bzty}"')

    result = " ".join(query)
    print(f'rs : {result}')
    return result


def selectSchList(useYn, pkgId):

    query = []
    query.append('SELECT            ')
    query.append('	PKG_ID          ')
    query.append('	,SCH_ID         ')
    query.append('	,SCH_JOB_TYPE   ')
    query.append('	,SCH_JOB        ')
    query.append('	,BZ_METHOD      ')
    query.append('	,SCH_DESC       ')
    query.append('	,USE_YN         ')
    query.append('	,REG_ID         ')
    query.append('	,UPD_ID         ')
    query.append('FROM TB_SK_PKG_SCH')
    query.append('WHERE 1=1 ')
    if(pkgId is not None):
        query.append(f'AND PKG_ID = "{pkgId}"')
    if (useYn is not None):
        query.append(f'AND USE_YN = "{useYn}"')

    return " ".join(query)


def saveSch(pkgId, skGroup, params):

    query = []
    query.append('UPDATE TB_SK_PKG_SCH SET')
    for index, key in enumerate(params):
        if index == 0:
            query.append(f'"{key}" = "{params[key]}"')
        else:
            query.append(f',"{key}" = "{params[key]}"')
    query.append('WHERE 1=1')
    query.append(f'AND PKG_ID = "{pkgId}"')
    query.append(f'AND SCH_ID = "{skGroup}"')

    result = " ".join(query)
    print(f'rs : {result}')
    return result


def delSch(pkgId, skgroup):

    query = []
    query.append('DELETE FROM TB_SK_PKG_SCH')
    query.append('WHERE 1=1')
    query.append(f'AND PKG_ID = "{pkgId}"')
    query.append(f'AND SCH_ID = "{skgroup}"')

    result = " ".join(query)
    print(f'rs : {result}')
    return result



def updateTbSkMsgVal(valId,val ):
    query = []
    query.append('UPDATE TB_SK_MSG_VAL SET  ')
    query.append(f'	VAL_DESC  = "{val}"          ')
    query.append('WHERE 1=1                 ')
    query.append(f'AND VAL_ID = "{valId}"           ')
    return " ".join(query)


def selectMsgBodyCnt(msgId,):
    query = []
    query.append('SELECT COUNT(1)		')
    query.append('FROM TB_SK_MSG_BODY ')
    query.append('WHERE 1=1           ')
    query.append(f'AND MSG_ID= "{msgId}"    ')
    return " ".join(query)

def selectMsgBodyDtCnt(msgId,valId, dtOrd):
    query = []
    query.append('SELECT COUNT(1)		')
    query.append('FROM TB_SK_MSG_BODY_DT ')
    query.append('WHERE 1=1           ')
    query.append(f'AND MSG_ID= "{msgId}"    ')
    query.append(f'AND MSG_DT_VAL_ID= "{msgId}"    ')
    query.append(f'AND MSG_DT_ORD= "{dtOrd}"    ')
    return " ".join(query)

def insertMsgBody(params):
    query = []
    keys = list(params.keys())
    values = [("" if str(v) is None else '""' if str(v) == "" else str(f"'{v}'")) for v in params.values()]
    query.append('INSERT INTO TB_SK_MSG_BODY (')
    query.append(','.join(keys))
    query.append(') VALUES(')
    query.append(','.join(values))
    query.append(')')
    result = " ".join(query)
    print(f'rs : {result}')
    return result

def insertMsgBodyDt(params):
    query = []
    keys = list(params.keys())
    values = [("" if str(v) is None else '""' if str(v) == "" else str(f"'{v}'")) for v in params.values()]
    query.append('INSERT INTO TB_SK_MSG_BODY_DT (')
    query.append(','.join(keys))
    query.append(') VALUES(')
    query.append(','.join(values))
    query.append(')')
    result = " ".join(query)
    print(f'rs : {result}')
    return result

def updateMsgBody(params ):
    key = params['MSG_ID']
    query = []
    query.append('UPDATE TB_SK_MSG_BODY SET  ')
    query.append(f'	MSG_KEY_TYPE  = "{params["MSG_KEY_TYPE"]}"          ')
    query.append(f'	,MSG_KEY_VAL  = "{params["MSG_KEY_VAL"]}"          ')
    query.append(f'	,MSG_DESC  = "{params["MSG_DESC"]}"          ')
    query.append(f'	,MSG_KEY_LENGTH  = "{params["MSG_KEY_LENGTH"]}"          ')
    query.append('WHERE 1=1                 ')
    query.append(f'AND MSG_ID = "{key}"           ')
    return " ".join(query)

def updateMsgBodyDt(params ):
    key = params['MSG_ID']
    key2 = params['MSG_DT_VAL_ID']
    key3 = params['MSG_DT_ORD']

    query = []
    query.append('UPDATE TB_SK_MSG_BODY_DT SET  ')
    query.append(f'	MSG_KEY_TYPE  = "{params["MSG_KEY_TYPE"]}"          ')
    query.append(f'	,MSG_KEY_VAL  = "{params["MSG_KEY_VAL"]}"          ')
    query.append(f'	,MSG_DESC  = "{params["MSG_DESC"]}"          ')
    query.append('WHERE 1=1                 ')
    query.append(f'AND MSG_ID = "{key}"           ')
    query.append(f'AND MSG_DT_VAL_ID = "{key2}"           ')
    query.append(f'AND MSG_DT_ORD = "{key3}"           ')

    return " ".join(query)


def deleteMsgBody(msgId ):
    query = []
    query.append('DELETE FROM TB_SK_MSG_BODY  ')
    query.append('WHERE 1=1                 ')
    query.append(f'AND MSG_ID = "{msgId}" ')
    return " ".join(query)

def deleteMsgBodyDt(msgId ):
    query = []
    query.append('DELETE FROM TB_SK_MSG_BODY_DT  ')
    query.append('WHERE 1=1                 ')
    query.append(f'AND MSG_ID = "{msgId}"    ')
    return " ".join(query)

def insertMsgVal(params):
    query = []
    keys = list(params.keys())
    values = [("" if str(v) is None else '""' if str(v) == "" else str(f"'{v}'")) for v in params.values()]
    query.append('INSERT INTO TB_SK_MSG_VAL (')
    query.append(','.join(keys))
    query.append(') VALUES(')
    query.append(','.join(values))
    query.append(')')
    result = " ".join(query)
    print(f'rs : {result}')
    return result