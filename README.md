# srt-gugg

SRT(수서고속철) 승차권을 자동으로 조회하고, 좌석이 열리면 자동으로 예매하는 봇입니다.
[SRT](https://pypi.org/project/SRT/) 비공식 파이썬 패키지를 사용해 SRT 홈페이지의
예매 절차(로그인 → 열차 조회 → 예약)를 자동화합니다.

> ⚠️ 이 봇은 SRT를 공식 지원하지 않는 리버스 엔지니어링 기반 라이브러리를 사용합니다.
> SRT 홈페이지 구조가 바뀌면 동작하지 않을 수 있으며, 과도하게 짧은 주기로 반복 조회하면
> 계정 제한이나 서비스 이용 약관 위반으로 이어질 수 있으니 책임은 사용자 본인에게 있습니다.

## 기능

- SRT 계정으로 로그인 후 원하는 구간/날짜/시간대의 열차를 반복 조회
- 일반석/특실 중 원하는 좌석 타입(또는 우선순위)으로 필터링
- 좌석이 열리면 자동으로 예약 시도, 성공 시 즉시 종료
- 세션 만료/일시적 오류 시 자동 재로그인 및 재시도
- (선택) 텔레그램으로 시작/성공 알림 전송

## 설치

```bash
pip install -r requirements.txt
```

## 설정

`.env.example`을 복사해 `.env` 파일을 만들고 값을 채워주세요.

```bash
cp .env.example .env
```

| 변수 | 설명 |
| --- | --- |
| `SRT_ID` | SRT 회원번호, 이메일 또는 휴대폰 번호 |
| `SRT_PASSWORD` | SRT 비밀번호 |
| `DEP_STATION` / `ARR_STATION` | 출발역 / 도착역 (예: 수서, 부산) |
| `TRAIN_DATE` | 예매 날짜 (`YYYYMMDD`) |
| `TIME_START` / `TIME_END` | 조회할 시간대 (`HHMMSS`) |
| `ADULT_COUNT` / `CHILD_COUNT` / `SENIOR_COUNT` | 승객 수 |
| `SEAT_TYPE` | `GENERAL_FIRST`(기본), `SPECIAL_FIRST`, `GENERAL_ONLY`, `SPECIAL_ONLY` |
| `CHECK_INTERVAL_MIN` / `CHECK_INTERVAL_MAX` | 조회 재시도 간격(초), 이 범위에서 무작위로 대기 |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` | (선택) 텔레그램 알림용 |

## 실행

```bash
python main.py
```

`.env`에 설정하지 않고 커맨드라인 인자로 구간/날짜만 바꿔서 실행할 수도 있습니다.

```bash
python main.py --dep 수서 --arr 부산 --date 20260710 --time-start 060000 --time-end 120000
```

예약에 성공하면 콘솔에 로그가 출력되고(텔레그램 설정 시 메시지도 전송되고) 프로세스가 종료됩니다.
실제 결제/좌석 배정은 SRT 앱 또는 홈페이지에서 마무리해야 할 수 있습니다.

## 테스트

```bash
pytest
```
