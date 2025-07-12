-- KEYS[1] - snake name
-- ARGV[1] - direction ('up', 'down', 'left', 'right')
-- ARGV[2] - random left position
-- ARGV[3] - random top position
-- ARGV[4] - sid

local name = KEYS[1]
local direction = ARGV[1]
local random_left = ARGV[2]
local random_top = ARGV[3]
local sid = ARGV[4]

-- Set direction
redis.call('SET', 'snake:'..name..':direction', direction)

-- Set sid
redis.call('SET', 'snake:'..name..':sid', sid)

-- Set initial block position
redis.call('HSET', 'snake:'..name..':block:1',
        'left', random_left,
        'top', random_top
)

return redis.status_reply('OK')