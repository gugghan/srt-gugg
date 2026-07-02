# srt-gugg

SRT(수서고속철) 승차권을 자동으로 조회하고, 좌석이 열리면 자동으로 예매하는 봇입니다.
[SRTrain](https://pypi.org/project/SRTrain/) 비공식 파이썬 패키지를 사용해 SRT 홈페이지의
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
| `MAX_RUN_SECONDS` | (선택) 이 시간(초)이 지나도 예매 못하면 종료. 비워두면 무한 반복 |
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

## GitHub Actions로 실행하기 (로컬 실행 없이 계속 돌리기)

로컬 PC 없이도 `.github/workflows/srt-reserve.yml` 워크플로우가 **5분마다 자동으로**
저장소를 열어 예매를 시도합니다. 무한 루프 대신 매 실행마다 최대 `MAX_RUN_SECONDS`
(기본 240초) 동안만 시도하고, 예매에 성공하면 워크플로우가 스스로 비활성화됩니다.

### 1. 시크릿(Secrets) 등록

저장소 **Settings → Secrets and variables → Actions → Secrets** 탭에서 등록:

| 이름 | 설명 |
| --- | --- |
| `SRT_ID` | SRT 로그인 아이디 |
| `SRT_PASSWORD` | SRT 비밀번호 |
| `TELEGRAM_BOT_TOKEN` | (선택) 텔레그램 알림용 |
| `TELEGRAM_CHAT_ID` | (선택) 텔레그램 알림용 |

### 2. 변수(Variables) 등록

같은 화면의 **Variables** 탭에서 등록 (예매마다 바뀌는 값이라 Secrets보다 수정이 쉬운 Variables 사용):

| 이름 | 예시 |
| --- | --- |
| `DEP_STATION` | 수서 |
| `ARR_STATION` | 부산 |
| `TRAIN_DATE` | 20260710 |
| `TIME_START` | 060000 |
| `TIME_END` | 120000 |
| `ADULT_COUNT` | 1 |
| `SEAT_TYPE` | GENERAL_FIRST |

### 3. 실행 확인

- Secrets/Variables를 등록하면 5분 간격 스케줄에 따라 자동 실행됩니다.
- 저장소의 **Actions** 탭에서 즉시 실행해보고 싶다면 `SRT 자동예매` 워크플로우 →
  **Run workflow** 버튼으로 수동 실행할 수 있습니다.
- 예매에 성공하면 다음 실행부터는 워크플로우가 자동으로 꺼져 있습니다(수동으로 다시
  켜려면 Actions 탭에서 워크플로우를 Enable 하세요).

> ⚠️ GitHub의 스케줄 실행은 5분 단위이며, 저장소 활동이 60일간 없으면 자동으로
> 비활성화될 수 있습니다. Private 저장소라면 Actions 실행 시간이 계정의 무료 사용량에
> 포함되니 참고하세요.

## 테스트

```bash
pytest
```
