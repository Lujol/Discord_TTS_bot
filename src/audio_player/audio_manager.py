import discord
import io
import asyncio


AudioData = str | bytes
QueueItem = tuple[AudioData, float] # [오디오 패스or데이터 , 속도]

class AudioManager:
    
    def __init__(self):
        self.queues : dict[int , list[QueueItem]] = {}
        self.boost :float = 0.3
    
            
    async def get_message_context(self , ctx: discord.Interaction|discord.Message ) :
        if isinstance(ctx,discord.Message ):
            user = ctx.author
            guild = ctx.guild
        else:
            assert isinstance(ctx, discord.Interaction)
            user = ctx.user
            guild = ctx.guild
        
        # 1. 메시지 작성자가 봇에 dm을 보내는 등 서버에서 작성하는 채팅이 아닌 경우
        if not guild or not isinstance(user, discord.Member):
            return None, None
        
        # 2. 메시지 작성자가 음성 채널에 존재하는가?
        if user.voice is None or user.voice.channel is None:
            return None, None
        
        # channel : 메시지 작성자가 들어가있는 음성 채널
        channel = user.voice.channel
        # vc : 해당 서버에 대한 봇의 음성 클라이언트
        vc = guild.voice_client

        
        # 3. 타입 명시
        if vc is not None and not isinstance(vc, discord.VoiceClient):
            return None, None
        
        return vc , channel 
        
    
    async def ready_and_playing(self, ctx: discord.Interaction|discord.Message, 
                                audio :str|bytes,
                                default_speed : float):
        
        # 1. 유효성 검사 및 vc, channel 추출
        vc , channel = await self.get_message_context(ctx)
        
        if channel is None:
            return 
        
        # 2.1 봇이 음성 채널에 존재하지 않는 경우 > 해당 채널에 입장
        if vc is None :
            vc = await channel.connect()
        
        # 2.2 봇이 다른 음성 채널에 존재 할 경우 > 이동
        elif  vc.channel != channel :
            await vc.move_to(channel)
            
        guild_id = channel.guild.id
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        
        if vc.is_playing() or vc.is_paused():
            queue_length = len(self.queues[guild_id])
            speed_boost = (queue_length + 1) * self.boost
            final_speed  = default_speed + speed_boost
            
            # FFmpeg atempo는 최대 2.0배속 권장
            if final_speed > 2.0:
                final_speed = 2.0
                
            # 큐에 튜플 형태로 저장 <오디오, 계산된 배속>
            self.queues[guild_id].append((audio, final_speed))
            return
        
        else:
            await self._play_audio_task(vc, guild_id, audio, default_speed)

    
    async def _play_audio_task(self, vc : discord.VoiceClient ,
                               guild_id : int, 
                                audio :str|bytes,
                                speed : float):
        
        # 배속 필터 설정
        ffmpeg_options = f'-filter:a "atempo={speed}"'
        
        def playing_callback(error):
            if error:
                raise Exception(f"[Error] 재생 처리 중 에러 발생 ! {error}" )
            
            # 큐에 남은 데이터가 있는지 확인
            if guild_id in self.queues and len(self.queues[guild_id]) > 0:
                next_audio, next_speed = self.queues[guild_id].pop(0)
                # callback 함수를 비동기로 할 수 없으므로 이벤트 루프 생성
                vc.loop.create_task(self._play_next_with_delay(vc, guild_id, next_audio, next_speed))
        
        #  재생
        try:
            if isinstance(audio, str):
            
                source = discord.FFmpegPCMAudio(audio, options=ffmpeg_options)
            
                
            else:
                isinstance(audio, bytes)
                audio_stream = io.BytesIO(audio)
            
                source = discord.FFmpegPCMAudio(audio_stream, pipe=True, options=ffmpeg_options)
            
            # after에 해당 오디오 실행 후 실행 할 playing_callback 넣음
            vc.play(source= source,after= playing_callback )
            
        except Exception as e:
            raise Exception(f"[Error] 재생 중 오류 발생 ! {e}" )
    
    async def _play_next_with_delay(self, vc : discord.VoiceClient ,
                               guild_id : int, 
                                audio :str|bytes,
                                speed : float):
            
        await asyncio.sleep(0.5) 
        
        # 다음 오디오 재생
        await self._play_audio_task(vc, guild_id, audio, speed)
        
        
        
    async def pause( self, ctx: discord.Interaction|discord.Message):
        # 1. 유효성 검사 및 vc, channel 추출 
        vc , channel = await self.get_message_context(ctx)
        
        # 2. 재생 중 이면, 일시정지
        if vc and vc.is_playing():
            vc.pause()
            
        else:
            return
        

    async def resume( self, ctx: discord.Interaction|discord.Message):
        
        # 1. 유효성 검사 및 vc, channel 추출
        vc , channel = await self.get_message_context(ctx)
        
        # 2. 일시 정지 중이면 다시 재생
        if vc and vc.is_paused():
            vc.resume()
            
        else:
            return
        

    async def stop( self,  ctx: discord.Interaction|discord.Message):
        # 1. 유효성 검사 및 vc, channel 추출 
        vc , channel = await self.get_message_context(ctx)
        
        # 2. 재생 중, 일시 정지 중이면 정지
        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()
        else:
            return