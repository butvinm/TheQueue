from os import getenv

from aiogram import Router

from .error import router as error_router
from .menu import router as menu_router
from .new_queue import router as new_queue_router
from .start import router as start_router

router = Router()
router.include_router(start_router)
router.include_router(menu_router)
router.include_router(new_queue_router)


if getenv('ENABLE_ERRORS_LOGS') == 'True':
    router.include_router(error_router)
