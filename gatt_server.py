from bluepy import btle
import time

# GATT 서버를 상속하는 사용자 정의 서버 클래스 정의
class CustomGattServer(btle.Peripheral):
    def __init__(self):
        super(CustomGattServer, self).__init__()

        # 서비스 생성
        self.service = btle.UUID("00001800-0000-1000-8000-00805f9b34fb")
        self.add_service(self.service)

        # 특성 생성 및 값 설정
        self.characteristic = btle.UUID("00002a00-0000-1000-8000-00805f9b34fb")
        self.property = btle.Characteristic(self.service, self.characteristic, btle.ADDR_TYPE_PUBLIC, btle.ADDR_TYPE_PUBLIC, "Hello, GATT!")

        # 속성 설정
        self.property.properties = btle.Characteristic.props["READ"]

# 메인 코드
if __name__ == '__main__':
    try:
        # 사용자 정의 GATT 서버 인스턴스 생성
        server = CustomGattServer()

        # 서버 실행
        while True:
            server.waitForNotifications(1.0)
    except KeyboardInterrupt:
        server.disconnect()
