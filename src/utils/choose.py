def choose(options, env, alter: list | None = None):
    check = alter if alter else options
    if not env in check:
        raise ValueError(f"{env} is not in {check}")
    return options[alter.index(env)] if alter else env
