from pydoc import cli
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
from function import function 
from os import system
import discord, asyncio 
import random

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event 
async def on_ready():
    system('cls')
    print("READY")
    DiscordComponents(client)

@client.event
async def on_message(message):
    if message.author.bot:
        return False
    
    color_data = {
        'pink': discord.utils.get(message.guild.roles, name="핑크"),
        'mint': discord.utils.get(message.guild.roles, name="민트"),
        'yellow': discord.utils.get(message.guild.roles, name="노랑"),
        'purple': discord.utils.get(message.guild.roles, name="보랑"),
        'orange': discord.utils.get(message.guild.roles, name="주황"),
        'red': discord.utils.get(message.guild.roles, name="빨강")
    }

    if message.content.startswith("!데이터생성"):
        if message.channel.id != 975737700311253035: #수정필요
            return None
        sql, woogi = function.join_sql()
        if sql:
            woogi.execute(f"SELECT * FROM user_info WHERE user_id = {message.author.id}")
            sql.commit()
            result = woogi.fetchone()
            if result is None:
                woogi.execute(f"INSERT INTO user_info (user_id, user_name, point, daily, daily_check) values({message.author.id}, '{message.author.name}', {1000}, {0}, {0})")
                sql.commit()
                sql.close()
                embed=discord.Embed(title=f"데이터 생성이 완료되었습니다")
                embed.add_field(name="보유 포인트", value=f"```1,000포인트```", inline=True)
                embed.add_field(name="출석일수", value=f"```0일```", inline=True)
                await message.reply(embed=embed)
            else:
                return await message.reply("> 데이터가 이미 존재합니다")
    elif message.content.startswith("!출석"):
        if message.channel.id != 975737700311253035: #수정필요
            return None
        sql, woogi = function.join_sql()
        if sql:
            data = function.check_data_user(message.author.id)
            if data:
                if data[4] == 1:
                    return await message.reply(f"> 이미 출석하셨습니다")
                
                new_point = 1000 # 출석시 지급할 포인트 ( 수정필요 )
                woogi.execute(f"UPDATE user_info SET daily_check = 1 WHERE user_id = {message.author.id}")
                woogi.execute(f"UPDATE user_info SET daily = {data[4] + 1} WHERE user_id = {message.author.id}")
                woogi.execute(f"UPDATE user_info SET point = {int(function.my_point(message.author.id)) + 1000} WHERE user_id = {message.author.id}")
                sql.commit()
                sql.close()
                await message.reply(f"> 출석체크 완료! 현재 출석일수 : {data[4] + 1}일")
            else:
                return await message.reply(f"> 데이터를 생성 후 다시 시도해주세요")
        else:
            return await message.reply(f"> 데이터베이스 접속 실패") 
    elif message.content.startswith("!내포인트"):
        data = function.my_point(message.author.id)
        if data:
            embed=discord.Embed(title=f"데이터 생성이 완료되었습니다")
            embed.add_field(name="보유 포인트", value=f"```{data}포인트```", inline=True)
            await message.reply(embed=embed)
        else:
            await message.reply("> 데이터를 생성 후 다시 시도해주세요")
            
    elif message.content.startswith("!색상표구매"):
        sql, woogi = function.join_sql()
        data = function.check_data_user(message.author.id)
        if not sql:
            return await message.reply(f"> 데이터베이스 접속 실패") 

        if not data:
            return await message.reply(f"> 데이터를 생성 후 다시 시도해주세요")

        check = await message.reply(f"어떤 색상을 구매할까요?",
            components = [
                Select(
                placeholder = "선택하기",
                    options = [
                        SelectOption(label = "💖 빨강", value = "빨강"),
                        SelectOption(label = "🧡 주황", value = "주황"),
                        SelectOption(label = "💛 노랑", value = "노랑"),
                        SelectOption(label = "🤹‍♂️ 민트", value = "민트"),
                        SelectOption(label = "💜 보랑", value = "보랑"),
                        SelectOption(label = "💗 핑크", value = "핑크"),
                        SelectOption(label = "❌ 취소", value = "취소"),
                    ]
                )
            ],
        )

        try:
            interaction = await client.wait_for("select_option", timeout=30)
            if interaction.values[0] == "취소":
                await check.delete()
                return await message.reply(embed=discord.Embed(description="구매가 취소되었습니다", color=0xff0000))
        except:
            await check.delete()
            return await message.reply("TIME OUT 시간초과로 인해 색상표 구매가 취소되었습니다")
        
        if interaction.values[0] == "빨강":
            await message.author.add_roles(color_data['red'])
            woogi.execute(f"UPDATE user_info SET red = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "주황":
            await message.author.add_roles(color_data['orange'])
            woogi.execute(f"UPDATE user_info SET orange = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "노랑":
            await message.author.add_roles(color_data['yellow'])
            woogi.execute(f"UPDATE user_info SET yellow = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "민트":
            await message.author.add_roles(color_data['mint'])
            woogi.execute(f"UPDATE user_info SET mint = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "보랑":
            await message.author.add_roles(color_data['purple'])
            woogi.execute(f"UPDATE user_info SET purple = 1 WHERE user_id = {message.author.id}")
        elif interaction.values[0] == "핑크":
            await message.author.add_roles(color_data['pink'])
            woogi.execute(f"UPDATE user_info SET pink = 1 WHERE user_id = {message.author.id}")

        await check.delete()
        await message.reply(f"{interaction.values[0]} 색상표가 구매되었습니다")
    
    elif message.content.startswith("!후기"):
        data = message.content.split()
        user_id = data[1].replace("<!@", "").replace("<@", "").replace(">", "")
        user = client.get_user(int(user_id))
        msg = message.content.replace(data[0], "").replace(data[1], "")

        channel = client.get_channel(975737700311253035) # 수정 필요 ( 후기 채널을 등록해주세요 )
        if message.channel == channel:
            if user == message.author:
                return await message.reply("자기 자신에게는 후기를 남길 수 없습니다")
            sql, woogi = function.join_sql()
            if not sql:
                return await message.reply(f"> 데이터베이스 접속 실패") 
            
            woogi.execute(f"SELECT * FROM user_review WHERE user_id = {user_id}")
            result = woogi.fetchone()
            count = 0
            if result is None:
                woogi.execute(f"INSERT INTO user_review(user_id, count) values({user_id}, 1)")
            else:
                count += int(result[1]) + 1
                woogi.execute(f"UPDATE user_review SET count = {int(result[1]) + 1} WHERE user_id = {user_id}")
            sql.commit()
            sql.close()
            await message.channel.send(embed=discord.Embed(title=f"", description=f"{message.author.mention}님이 {user.mention}님에게 후기를 남기셨습니다\n\n**'{msg}'**\n\n> **{user.mention}님의 총 후기 개수 : {count}개**"))
    elif message.content.startswith("!주사위"):
        data = function.my_point(message.author.id)
        betting_point = int(message.content.replace("!주사위", "")) or 0
        plus = 1.5
        if not data:
            return await message.reply("데이터 생성 후 다시 시도해주세요\n\n> !데이터생성")
        
        data = int(data)

        if data < int(betting_point):
            return await message.reply("포인트 부족")

        if betting_point <= 0:
            return await message.reply("베팅 포인트를 정확히 적어주세요")
        user_random = random.randint(1, 6)
        bot_random = random.randint(1, 6)
        function.update_my_point(message.author.id, betting_point)
        if user_random == bot_random:
            await message.reply(f"**비겼습니다**\n\n> 내 주사위 : {user_random}\n\n> 봇 주사위 : {bot_random}\n\n> 내 포인트 : {function.my_point(message.author.id)}")
        elif user_random > bot_random:
            function.plus_my_point(message.author.id, betting_point * plus)
            await message.reply(f"**이겼습니다**\n\n> 내 주사위 : {user_random}\n\n> 봇 주사위 : {bot_random}\n\n> 내 포인트 : {function.my_point(message.author.id)}")
        else:
            await message.reply(f"**졌습니다**\n\n> 내 주사위 : {user_random}\n\n> 봇 주사위 : {bot_random}\n\n> 내 포인트 : {function.my_point(message.author.id)}")


client.run("")