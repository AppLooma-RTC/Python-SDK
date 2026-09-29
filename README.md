# applooma (Python)

```bash
pip install applooma
```

```python
from applooma import AppServerClient

applooma = AppServerClient(api_key="...", api_secret="...")
res = applooma.create_token(room_name="room1", identity="user1", role="host")
# res["token"], res["wsUrl"]
```

## Server-side participants (bots)

Bots live in a separate distribution, `applooma-bot`, so this token SDK stays
pure Python with no native code. It ships prebuilt wheels (through its
dependency `applooma-rtc-native`) for Linux x86_64/aarch64, macOS arm64/x86_64
and Windows x64, CPython 3.9+, so `pip install` never needs a compiler. Beta
(0.1.0), with the same API and message format as the Node bot
`@applooma/rtc-server-participant`.

```bash
pip install applooma applooma-bot
```

```python
from applooma import AppServerClient
from applooma_bot import AppBot

t = AppServerClient(api_key="...", api_secret="...").create_token(
    room_name="room1", identity="echo-bot", role="host")

bot = await AppBot.join(url=t["wsUrl"], token=t["token"],
                        receive_sample_rate=48000, receive_channels=1)

@bot.on("audio_frame")
async def echo(frame, user):          # frame.data: interleaved 16-bit PCM bytes
    await bot.publish_audio(frame)

@bot.on("message")
async def on_message(msg):
    await bot.send_message(f"echo: {msg.text}")

await bot.leave()
```

- `publish_audio(AppAudioFrame(data, sample_rate, channels))` and `publish_video(AppVideoFrame(data, width, height, "i420" | "rgba"))`.
- Events `audio_frame`, `video_frame`, `message`, `user_joined`, `user_left`, `disconnected`, `error`.
- Errors are `AppBotError` with `.code`: `unsupported_platform`, `join_failed`, `not_joined`, `invalid_frame`, `send_failed`.

Docs: https://docs.applooma.dev/sdk/server-participant#python

Docs: https://applooma.dev/dashboard/docs
