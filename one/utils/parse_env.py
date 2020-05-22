def parse_env(env):
    lines = env.split("\n")
    environment = {}

    for line in lines:
        if line.strip() == "" or line[0] == '#':
            continue

        parse_line = line.strip().split('=', 1)
        if len(parse_line) == 2:
            k, v = parse_line
            environment[k] = v

    return environment
