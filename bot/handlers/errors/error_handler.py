import traceback
from data import config
from loader import bot

from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)

from loader import dp
from utils.misc.logging import logger


@dp.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        logger.debug('Can\'t demote chat creator')
        for admin_id in config.ADMINS:
            await bot.send_message(admin_id, 'Can\'t demote chat creator')
        return True

    if isinstance(exception, MessageNotModified):
        logger.debug('Message is not modified')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logger.debug('Message cant be deleted')
        for admin_id in config.ADMINS:
            await bot.send_message(admin_id, 'Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logger.debug('Message to delete not found')
        for admin_id in config.ADMINS:
            await bot.send_message(admin_id, 'Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logger.debug('MessageTextIsEmpty')
        for admin_id in config.ADMINS:
            await bot.send_message(admin_id, 'MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logger.info(f'Unauthorized: {exception}')
        for admin_id in config.ADMINS:
            await bot.send_message(admin_id, f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logger.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        for admin_id in config.ADMINS:
            await bot.send_message(admin_id, f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logger.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        for admin_id in config.ADMINS:
            await bot.send_message(admin_id, f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        logger.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        for admin_id in config.ADMINS:
            await bot.send_message(admin_id, f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        logger.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        for admin_id in config.ADMINS:
            await bot.send_message(admin_id, f'CantParseEntities: {exception} \nUpdate: {update}')
        return True

    try:
        raise exception
    except:
        exception_traceback = traceback.format_exc()

    logger.exception(f'Update: {update} \n{exception_traceback}')
    for admin_id in config.ADMINS:
        await bot.send_message(admin_id, f'Update: {update} \n{exception_traceback}')
