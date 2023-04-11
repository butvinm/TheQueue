from os import getenv

from aiogram import Router

from .enroll_queue import router as enroll_queue_router
from .error import router as error_router
from .menu import router as menu_router
from .my_queues import router as my_queues_router
from .new_queue import router as new_queue_router
from .queue_manage import router as queue_manage_router
from .queue_page import router as queue_page_router
from .start import router as start_router

router = Router()
router.include_router(start_router)
router.include_router(menu_router)
router.include_router(new_queue_router)
router.include_router(enroll_queue_router)
router.include_router(queue_page_router)
router.include_router(my_queues_router)
router.include_router(queue_manage_router)

if getenv('ENABLE_ERRORS_LOGS') == 'True':
    router.include_router(error_router)
