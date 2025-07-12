-- KEYS[1] - snake name
-- ARGS[1] - new direction

local snake_name = KEYS[1]
local new_direction = ARGS[1]

redis.call('HSET', 'snake:'..snake_name..':direction', new_direction)