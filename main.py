import db

conn = db.DbConnection.dbconnHadwh("")
connerp = db.DbConnection.dbconnErp("")


sql = 'select ROWID,RECORDED_TIME,MOBILE_NO,case when USERID is null then ' \
      '(select EMP_NUMBER from SLT_EMP_TP where substr(MOBILE_NO,-9)=substr(TPNO,-9)) ' \
      'else USERID end as USERID, USER_ACTIVITY, IN_SYSTEM from ATTENDANCE_202204 ' \
      'where DSTATUS is null '
c = conn.cursor()
c.execute(sql)

for row in c:
    ROW_ID,RECORDED_TIME, MOBILE_NO, USERID, USER_ACTIVITY, IN_SYSTEM = row
    print(ROW_ID,RECORDED_TIME, MOBILE_NO, USERID, USER_ACTIVITY, IN_SYSTEM)

    matches = ["IN", "OUT"]

    if any(x in USER_ACTIVITY for x in matches):
        print('success')
        sqlerp = "INSERT INTO XXERP.HR_MOB_ATTENDANCE VALUES ( :RECORDED_TIME,:MOBILE_NO,:USERID,:USER_ACTIVITY,:IN_SYSTEM,:DSTATUS)"
        with connerp.cursor() as cursor:
            cursor.execute(sqlerp, [RECORDED_TIME, MOBILE_NO, USERID, USER_ACTIVITY, IN_SYSTEM, '0'])
            connerp.commit()

        sqlhadwh = "update ATTENDANCE_202204 set DSTATUS=:DSTATUS where  ROWID= :ROW_ID and DSTATUS is null"
        with conn.cursor() as cursor2:
            cursor2.execute(sqlhadwh, ["10", ROW_ID])
            conn.commit()

    else:
        print('failed')
        sqlhadwh = "update ATTENDANCE_202204 set DSTATUS=:DSTATUS where  ROWID= :ROW_ID and DSTATUS is null"
        with conn.cursor() as cursor2:
            cursor2.execute(sqlhadwh, ["20", ROW_ID])
            conn.commit()

