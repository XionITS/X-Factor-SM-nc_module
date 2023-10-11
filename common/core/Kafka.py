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
    cursor.execute("INSERT INTO common_xfactor_ncdb (column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12, column13) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,)"
                   , (data['value1'], data['value2'], data['value3'], data['value4'], data['value5'], data['value6'], data['value7'], data['value8'], data['value9'], data['value10'], data['value11'], data['value12'], data['value13']))

    conn.commit()
    cursor.close()
    conn.close()


def Kafka_Con():
    print("Kafka 연결")
    # Kafka 설정
    kafka_config = {
        'bootstrap.servers': '172.20.5.26:9092',  # Kafka 브로커 IP와 포트
        'group.id': 'my-consumer-group',
        'auto.offset.reset': 'earliest'
    }
    # Kafka 토픽 설정
    kafka_topic = 'stg.korea.nck.employee.entire'
    #[dev./qa./stg./없음]korea.[companyCode].employee.entire

    # Kafka 소비자 생성
    consumer = Consumer(kafka_config)
    consumer.subscribe([kafka_topic])

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
            data = eval(msg.value().decode('utf-8'))
            save_to_postgresql(data)

    # 소비자 종료
    consumer.close()