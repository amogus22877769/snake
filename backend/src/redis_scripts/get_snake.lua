-- ARGV[1] - snake sid

local snake_sid = ARGV[1]
local function get_snake_name(block_key)
    local snake = string.sub(block_key, 7, -1)
    local snake_name = ''
    for i = 1, #snake do
        local c = string.sub(snake, i, i)
        if c == ':' then
            break
        end
        snake_name = snake_name..c
    end
    return snake_name
end
local snake_name = ''
local sid_keys = redis.call('KEYS', 'snake:*:sid')
for _, sid_key in ipairs(sid_keys) do
    local sid = redis.call('GET', sid_key)
    if sid == snake_sid then
        snake_name = get_snake_name(sid_key)
        break
    end
end

return snake_name