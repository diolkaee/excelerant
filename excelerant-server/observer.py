import asyncio
from typing import Awaitable, Callable, Optional, TypeVar

T = TypeVar('T')


def buildObserver(updateFunction: Callable[[T], Awaitable[None]], delay: Optional[int] = 1) -> Callable[[Callable[[T], Awaitable[None]]], Awaitable[None]]:
    '''Creates an observer that polls an update function and invokes a callback whenever the value changes'''
    async def observer(callback):
        lastValue = None

        while (True):
            currentValue = updateFunction()
            if (currentValue != lastValue):
                await callback(currentValue)
                lastValue = currentValue
            await asyncio.sleep(delay)

    return observer
