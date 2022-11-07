CMD_DESC = (
    # cmd, inline description, long description

    # /-commands (bot info commands)
    # not for use in group chat
    ('start', "запустить справку о боте",
     "...праздный ум — мастерская дьявола 😈"),
    ('help', 'путеводитель',
     'если ты читаешь это сообщение — ты умеешь пользоваться командой /help\n\n'
     'другой способ получить справку о команде — вызвать её саму в ЭТОМ диалоге\n'
     'команды делятся на несколько типов, для наглядности они отличаются префиксами:\n'
     '! — модераторские команды ()'),
    ('whoami', 'получить айди своего тг-аккаунта', None),
    # !-commands (moderator's commands)
    # for use in group chat only
    ('rr', "random read-only",
     ''),
    # $-commands
    # %-commands
    # &-commands
)
