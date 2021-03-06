import random

from discord.ext import commands


def test_username(nickname: str, ctx: commands.Context) -> list:
    errors = []
    string_to_test = ctx.author.display_name if len(nickname) == 0 else nickname
    if len(nickname) == 0:
        if ctx.author.nick:
            verbal_test = "nickname"
        else:
            verbal_test = "username"
    else:
        verbal_test = "custom name"

    if len(string_to_test) < 5:
        errors.append(f"Your {verbal_test} is too short. It need to be at least 5 characters.")
    if len(string_to_test) > 25:
        errors.append(f"Your {verbal_test} is too long. It needs to be under 25 characters.")
    if not string_to_test.isalpha():
        errors.append(f"Please only use alphabetical characters in your {verbal_test}.")
    return errors


async def check_has_gift(db, author_id: int) -> bool:
    async with db.acquire() as conn:
        check = await conn.fetchval("""
        SELECT EXISTS (
        SELECT 1
        FROM gifts
        WHERE active = TRUE and user_id = $1
        )
        """, author_id)
    return check


def secret_substring(name: str) -> str:
    length = random.randint(3, 4)
    start = random.randint(0, len(name) - length)
    result = name[start:start + length]
    return f"Part of the label has been cut off! The remaining label contains: `{result}`"


def secret_smudge(name: str) -> str:
    smudged = random.sample(range(len(name)), round(len(name) * .7))
    result = list(name)
    for i in smudged:
        result[i] = '#'
    result = ''.join(result)
    return f"The label has smudges on it. You can only make out the following letters: `{result}`"


def secret_scramble(name: str) -> str:
    scrambled = list(name)
    random.shuffle(scrambled)
    result = ''.join(scrambled)
    return f"Someone scrambled the letters on the label. It reads: `{result}`"


def secret_string_wrapper(secret_member: str) -> str:
    secret_array = [secret_scramble, secret_substring, secret_smudge]
    secret_string = random.choice(secret_array)(secret_member)
    return secret_string
