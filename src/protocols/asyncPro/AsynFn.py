import asyncio
import random
import time

# --- 일반적인 에코 핸들러 (서버 코루틴) ---
async def handle_echo(reader, writer):
    addr = writer.get_extra_info('peername')
    # 서버 포트를 식별하기 위해 writer.get_extra_info('sockname') 사용
    server_port = writer.get_extra_info('sockname')[1]
    print(f"[서버:{server_port}] 클라이언트 {addr} 연결됨")

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"[서버:{server_port}] 클라이언트 {addr} 연결 종료 요청.")
                break

            message = data.decode()
            print(f"[서버:{server_port}] {addr}로부터 '{message}' 수신")
            response = f"Echo from {server_port}: {message}"
            writer.write(response.encode())
            await writer.drain()
            await asyncio.sleep(0.001)

    except asyncio.CancelledError:
        print(f"[서버:{server_port}] 클라이언트 {addr} 처리 취소됨.")
    except ConnectionResetError:
        print(f"[서버:{server_port}] 클라이언트 {addr} 강제 연결 끊김.")
    except Exception as e:
        print(f"[서버:{server_port}] 클라이언트 {addr} 처리 중 오류 발생: {e}")
    finally:
        if writer and not writer.is_closing():
            print(f"[서버:{server_port}] 소켓 닫음.")
            writer.close()
            await writer.wait_closed()

# --- 서버 시작 코루틴 ---
async def start_single_server_instance(host, port):
    server = await asyncio.start_server(handle_echo, host, port)
    server_addr = server.sockets[0].getsockname()
    print(f"[서버 인스턴스] {server_addr}에서 서버 시작됨...")
    async with server:
        await server.serve_forever()

# --- 클라이언트 코루틴 ---
async def run_single_client_instance(host, port, client_id):
    reader, writer = None, None
    try:
        print(f"[클라이언트 {client_id}] 서버 {host}:{port}에 연결 시도 중...")
        reader, writer = await asyncio.open_connection(host, port)
        addr = writer.get_extra_info('peername')
        print(f"[클라이언트 {client_id}] 서버 {addr}에 연결됨.")

        message_count = 0
        while True:
            message_count += 1
            message = f"Client {client_id} to Port {port} - Msg {message_count}"
            print(f"[클라이언트 {client_id}] '{message}' 전송 중...")
            writer.write(message.encode())
            await writer.drain()

            data = await reader.read(1024)
            if not data:
                print(f"[클라이언트 {client_id}] 서버가 연결을 끊었습니다.")
                break

            response = data.decode()
            print(f"[클라이언트 {client_id}] 서버로부터 '{response}' 수신")

            await asyncio.sleep(random.uniform(1, 3))

    except ConnectionRefusedError:
        print(f"[클라이언트 {client_id}] 서버 {host}:{port} 연결 거부됨. 서버가 실행 중인지 확인하세요.")
    except ConnectionResetError:
        print(f"[클라이언트 {client_id}] 서버 {host}:{port}에 의해 강제 연결 끊김.")
    except asyncio.CancelledError:
        print(f"[클라이언트 {client_id}] 작업 취소됨.")
    except Exception as e:
        print(f"[클라이언트 {client_id}] 오류 발생: {e}")
    finally:
        if writer and not writer.is_closing():
            print(f"[클라이언트 {client_id}] 소켓 닫음.")
            writer.close()
            await writer.wait_closed()

# --- 메인 코루틴: 여러 서버와 클라이언트 시작 ---
async def main():
    HOST = '127.0.0.1'
    SERVER_PORTS = [8888, 8889] # 여러 개의 서버 포트 설정
    CLIENTS_PER_SERVER = 2 # 각 서버에 연결할 클라이언트 수
    SIMULATION_DURATION = 15 # 시뮬레이션 실행 시간 (초)

    all_tasks = []

    # 1. N개의 서버 인스턴스 시작
    print("--- 여러 서버 인스턴스 시작 ---")
    for port in SERVER_PORTS:
        server_task = asyncio.create_task(start_single_server_instance(HOST, port))
        all_tasks.append(server_task)

    # 서버들이 완전히 시작될 시간을 약간 기다려줍니다.
    await asyncio.sleep(1)

    # 2. 각 서버에 연결하는 N개의 클라이언트 태스크 시작
    print("\n--- 각 서버에 연결하는 클라이언트 태스크 시작 ---")
    client_id_counter = 1
    for port in SERVER_PORTS:
        for _ in range(CLIENTS_PER_SERVER):
            client_task = asyncio.create_task(run_single_client_instance(HOST, port, client_id_counter))
            all_tasks.append(client_task)
            client_id_counter += 1

    print(f"\n[메인] 모든 서버와 클라이언트가 단일 스레드 내에서 {SIMULATION_DURATION}초 동안 실행됩니다...")

    # 3. 지정된 시간 동안 시스템 실행 유지
    await asyncio.sleep(SIMULATION_DURATION)

    print(f"\n[메인] {SIMULATION_DURATION}초 경과. 모든 태스크 종료 중...")

    # 4. 모든 태스크 종료 요청
    # all_tasks 리스트에 서버 태스크와 클라이언트 태스크가 모두 포함되어 있습니다.
    for task in all_tasks:
        task.cancel()

    # 모든 태스크가 종료될 때까지 기다림
    await asyncio.gather(*all_tasks, return_exceptions=True)

    print("[메인] 모든 서버 및 클라이언트 태스크 종료 완료.")

# if __name__ == "__main__":
#     start_time = time.time()
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print("\n[메인] 사용자가 프로그램 종료를 요청했습니다.")
#     end_time = time.time()
#     print(f"\n총 실행 시간: {end_time - start_time:.2f} 초")