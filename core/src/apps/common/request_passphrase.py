from micropython import const

from trezor import wire
from trezor.messages.PassphraseAck import PassphraseAck
from trezor.messages.PassphraseRequest import PassphraseRequest
from trezor.ui.passphrase import CANCELLED, PassphraseKeyboard

from apps.common.storage import device as storage_device

if __debug__:
    from apps.debug import input_signal

_MAX_PASSPHRASE_LEN = const(50)


async def protect_by_passphrase(ctx: wire.Context) -> str:
    # TODO: rename to get_passphrase
    if storage_device.has_passphrase():
        return await request_passphrase(ctx)
    else:
        return ""


async def request_passphrase(ctx: wire.Context) -> str:
    request = PassphraseRequest()
    ack = await ctx.call(request, PassphraseAck)
    if ack.on_device:
        if ack.passphrase is not None:
            raise wire.ProcessError("Passphrase provided when it should not be")
        passphrase = await request_passphrase_on_device(ctx)
    else:
        if ack.passphrase is None:
            raise wire.ProcessError("Passphrase not provided")
        passphrase = ack.passphrase

    if len(passphrase) > _MAX_PASSPHRASE_LEN:
        raise wire.DataError("Maximum passphrase length is %d" % _MAX_PASSPHRASE_LEN)

    return passphrase


async def request_passphrase_on_device(ctx: wire.Context) -> str:
    keyboard = PassphraseKeyboard("Enter passphrase", _MAX_PASSPHRASE_LEN)
    if __debug__:
        passphrase = await ctx.wait(keyboard, input_signal())
    else:
        passphrase = await ctx.wait(keyboard)
    if passphrase is CANCELLED:
        raise wire.ActionCancelled("Passphrase entry cancelled")

    assert isinstance(passphrase, str)

    return passphrase
