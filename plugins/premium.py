from pyrogram import Client, filters
from database.db import db  
from info import LOG_CHANNEL, ADMINS

@Client.on_message(filters.command("add") & filters.user(ADMINS))
async def add_premium_command(client, message):
    try:
        args = message.text.split()
        if len(args) < 4:
            return await message.reply_text("❌ **Format:** `/add <user_id> <time_value> <time_unit>`\n**Example:** `/add 123456 30 days`")

        user_id = int(args[1])
        time_value = int(args[2])
        time_unit = args[3].lower()
        
        expiry = await db.add_premium_users(user_id, time_value, time_unit)
        
        # ✅ User Notification
        await client.send_message(
            user_id,
            f"🎉 **Congratulations!**\n"
            f"Your **Premium Membership** has been activated! 🚀\n"
            f"📅 **Valid Until:** `{expiry}`\n"
            f"Enjoy your exclusive perks! 💎"
        )
        
        # ✅ Log Channel Notification
        user = await client.get_users(user_id)
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        log_message = (
            f"✅ **Premium Activated**\n"
            f"👤 **User:** {mention} (`{user_id}`)\n"
            f"📅 **Expiry:** `{expiry}`\n"
            f"💎 **Premium Status:** **Active**"
        )

        await client.send_message(LOG_CHANNEL, log_message)
        
        # ✅ Reply in Chat (Same as Log)
        await message.reply_text(log_message)

    except ValueError:
        await message.reply_text("❌ **Invalid input format!** Use numbers correctly.")
    except Exception as e:
        print(f"❌ Error: {e}")
        await message.reply_text("❌ **Error adding premium user!**")

@Client.on_message(filters.command("remove") & filters.user(ADMINS))
async def remove_premium_command(client, message):
    try:
        args = message.text.split()
        if len(args) < 2:
            return await message.reply_text("❌ **Format:** `/remove <user_id>`")

        user_id = int(args[1])

        # ✅ First, check if the user has an active plan
        expiry = await db.check_user_premium(user_id)

        if not expiry:
            return await message.reply_text(f"🚀 **User `{user_id}` is not a premium member!** No need to remove.")

        # ✅ Remove premium access
        await db.remove_premium_access(user_id)

        # ✅ User Notification
        await client.send_message(
            user_id,
            "⚠️ **Premium Membership Removed**\n"
            "Your premium plan has been **cancelled**. 😞\n"
            "To re-activate, contact support or use `/plan`."
        )

        # ✅ Log Channel Notification
        user = await client.get_users(user_id)
        mention = f"[{user.first_name}](tg://user?id={user.id})"
        log_message = (
            f"❌ **Premium Removed**\n"
            f"👤 **User:** {mention} (`{user_id}`)\n"
            f"💎 **Premium Status:** ❌ **Removed**"
        )

        await client.send_message(LOG_CHANNEL, log_message)

        # ✅ Reply in Chat (Same as Log)
        await message.reply_text(log_message)

    except Exception as e:
        print(e)
        await message.reply_text("❌ **Error removing premium user!**")


@Client.on_message(filters.command("myplan"))
async def my_plan(client, message):
    user_id = message.from_user.id
    expiry = await db.check_user_premium(user_id)

    if expiry:
        await message.reply_text(
            f"👑 **Premium Membership Details** 👑\n\n"
            f"🔹 **User ID:** `{user_id}`\n"
            f"🔹 **Status:** ✅ **Active**\n"
            f"🔹 **Expiry Date:** `{expiry}`\n\n"
            f"Enjoy your premium perks! 🚀"
        )
    else:
        await message.reply_text("🚀 **You don't have an active premium plan!**\nUse `/plan` to see available options.")

@Client.on_message(filters.command("check") & filters.user(ADMINS))
async def check_premium(client, message):
    try:
        args = message.text.split()
        if len(args) < 2:
            return await message.reply_text("❌ **Format:** `/check <user_id>`")

        user_id = int(args[1])
        expiry = await db.check_user_premium(user_id)

        if expiry:
            await message.reply_text(
                f"👑 **Premium Status Check** 👑\n\n"
                f"🔹 **User ID:** `{user_id}`\n"
                f"🔹 **Status:** ✅ **Active**\n"
                f"🔹 **Expiry Date:** `{expiry}`\n\n"
                f"Enjoy your premium perks! 🚀"
            )
        else:
            await message.reply_text(
                f"🚀 **User `{user_id}` is not a premium member!**\nThey can check `/plan` for details."
            )

    except ValueError:
        await message.reply_text("❌ **Invalid user ID format!**")
    except Exception as e:
        print(f"❌ Error: {e}")
        await message.reply_text("❌ **Error checking premium status!**")
        
