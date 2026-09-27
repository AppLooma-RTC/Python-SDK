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

## Server-side participants (bots): plan

Not available yet. This section describes what is planned, so you can design
for it. The Node equivalent, `@applooma/rtc-server-participant`, ships today
as a 0.1.0 beta.

**Package.** A separate distribution, `applooma-rtc-agent`, so this token SDK
stays pure Python with no native code. It will ship prebuilt wheels for
linux-x64, linux-arm64, macOS arm64 and x64, and Windows x64 (CPython 3.9+),
so `pip install` never needs a compiler.

**API**, asyncio-first and matching the Node bot:

```python
from applooma import AppServerClient
from applooma_rtc_agent import AppBot

token = AppServerClient(api_key="...", api_secret="...").create_token(
    room_name="room1", identity="echo-bot", role="host")

bot = await AppBot.join(url=token["wsUrl"], token=token["token"],
                        receive_sample_rate=48000, receive_channels=1)

@bot.on("audio_frame")
async def echo(frame, user):          # frame.data: 16-bit PCM (bytes / numpy int16)
    await bot.publish_audio(frame)

@bot.on("message")
async def on_message(msg):
    await bot.send_message(f"echo: {msg.text}")

await bot.leave()
```

- `publish_audio(pcm, sample_rate, channels)` and `publish_video(data, width, height, format="i420" | "rgba")`.
- Events `audio_frame`, `video_frame`, `message`, `user_joined`, `user_left`, `disconnected`.
- Optional `numpy` integration: frames exposed as arrays without copying.
- `async for frame in bot.audio_frames(uid)` as an alternative to callbacks, for pipelines such as speech-to-text.

**Milestones.**
1. Wrap the same prebuilt native media stack the Node bot uses, behind our own
   types and error messages; audio in and out plus messages.
2. Video in and out (I420 / RGBA), numpy views.
3. Helpers for voice agents: voice activity detection hooks and a resampler.
4. Publish to PyPI as beta once the Node bot's API is stable at 1.0.

Docs: https://applooma.dev/dashboard/docs
