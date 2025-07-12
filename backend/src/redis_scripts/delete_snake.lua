-- ARGV[1] - sid

local sid = ARGV[1]

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
local function delete_snake(block_key)
    local snake_name = get_snake_name(block_key)
    local snake_keys = redis.call('KEYS', 'snake:'..snake_name..':*')
    for _, snake_key in ipairs(snake_keys) do
        redis.call('DEL', snake_key)
    end
    table.insert(events, {
        type = 'deleted',
        value = snake_name,
    })
end

local sid_keys = redis.call('KEYS', 'snake:*:sid')
for _, sid_key in ipairs(sid_keys) do
    if sid == redis.call('GET', sid_key) then
        delete_snake(sid_key)
    end
end