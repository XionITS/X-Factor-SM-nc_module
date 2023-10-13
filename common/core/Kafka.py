import json

from confluent_kafka import Consumer, KafkaError
import psycopg2


#계정 : nch.tanium.tadmin

#환경 DEV/QA/STG/LIVE

#법인
#NCK - (주)엔씨소프트
#DINOS - (주)엔씨다이노스
#NCITS - (주)엔씨아이티에스
#NCSS - (주)엔씨소프트서비스
#NCCF - NC문화재단
#KLAP - (주)클렙

#토픽
#임직원	[dev./qa./stg./없음]korea.[companyCode].employee
#임직원 전체	[dev./qa./stg./없음]korea.[companyCode].employee.entire
#부서	[dev./qa./stg./없음]korea.[companyCode].department
#부서 전체	[dev./qa./stg./없음]korea.[companyCode].department.entire
#발령	[dev./qa./stg./없음]korea.[companyCode].actchange
#오류	[dev./qa./stg./없음]korea.gis.mbwkr.errors

#DEV/QA 환경 : 172.20.5.26:9092,172.20.5.97:9092,172.20.5.98:9092
#비번 : MwSxXdsfA16LJ (DEV), iZU0biWFH8XK9 (QA)

#STG 환경 : 172.20.5.94:9092,172.20.5.100:9092,172.20.5.101:9092
#비번 : ScaRNSs80iFLo (STG)
#LIVE 환경 : 172.20.5.231:9092,172.20.5.232:9092,172.20.5.233:9092

#비번 : mb475g4dvGQzQ (LIVE)

# PostgreSQL에 데이터 저장
def save_to_postgresql(data):
    # PostgreSQL 연결 설정
    pg_config = {
        'dbname': 'ncsm',
        'user': 'postgres',
        'password': 'psql',
        'host': '172.20.161.64',
        'port': '5432'
    }
    conn = psycopg2.connect(**pg_config)
    cursor = conn.cursor()

    # SQL 쿼리를 사용하여 데이터를 PostgreSQL에 저장
    try:
        cursor.execute("""INSERT INTO common_xfactor_ncdb ("companyCode", "userName", "userNameEn", "userId", "email", "empNo", "joinDate", "retireDate", "deptCode", "deptName", "managerUserName", "managerUserId", "managerEmpNo")
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                       , (data.get('companyCode'), data.get('userName'), data.get('userNameEn'), data.get('userId'), data.get('email'), data.get('empNo'), data.get('joinDate'), data.get('retireDate'), data.get('deptCode'), data.get('deptName'), data.get('managerUserName'), data.get('managerUserId'), data.get('managerEmpNo')))
    except Exception as e:
        print(e)
    conn.commit()
    cursor.close()
    conn.close()


def Kafka_Con():
    pg_config = {
        'dbname': 'ncsm',
        'user': 'postgres',
        'password': 'psql',
        'host': '172.20.161.64',
        'port': '5432'
    }
    conn = psycopg2.connect(**pg_config)
    cursor = conn.cursor()
    try:
        cursor.execute("TRUNCATE TABLE common_xfactor_ncdb")
    except Exception as e:
        print(e)

    print("Kafka 연결1")
    # Kafka 설정
    kafka_config = {
        'bootstrap.servers': '172.20.5.26:9092',  # Kafka 브로커 IP와 포트
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest',
    }
    # Kafka 토픽 설정
    kafka_topic = 'stg.korea.nck.employee.entire'
    print("Kafka 연결2")
    #[dev./qa./stg./없음]korea.[companyCode].employee.entire

    # Kafka 소비자 생성
    consumer = Consumer(kafka_config)
    consumer.subscribe([kafka_topic])
    print("Kafka 연결3")

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('Reached end of partition')
            else:
                print('Error while consuming message: {}'.format(msg.error()))
        else:
            # Kafka에서 받은 메시지를 처리
            data = msg.value().decode('utf-8')
            message = json.loads(data)
            payload = message.get('payload')
            save_to_postgresql(payload)

    print("Kafka 연결4")
    # 소비자 종료
    consumer.close()
