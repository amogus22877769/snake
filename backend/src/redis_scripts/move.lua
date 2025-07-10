-- Delete old blocks for this snake
redis.call('DEL', 'lua:debug:logs')
local function debug_log(message)
    redis.call('RPUSH', 'lua:debug:logs', message)
end
local function get_block_number(key, snake_key_len)
    return tonumber(string.sub(key, snake_key_len + 8, #key))
end
local function compare_blocks_keys(snake_key_len)
    local function inner(key1, key2)
        return get_block_number(key1, snake_key_len) > get_block_number(key2, snake_key_len)
    end
    return inner
end
local snakes = redis.call('KEYS', 'snake:*:direction')
for _, snake in ipairs(snakes) do
    local snake_key = string.sub(snake,1, -11)
    local direction = redis.call('GET', snake)
    local blocks_keys = redis.call('KEYS', snake_key..':block:*')
    table.sort(blocks_keys, compare_blocks_keys(#snake_key))
    local first_block_left = redis.call('HGET', blocks_keys[#blocks_keys], 'left')
    local first_block_top = redis.call('HGET', blocks_keys[#blocks_keys], 'top')
    for index, block_key in ipairs(blocks_keys) do
        local this_block_left = redis.call('HGET', block_key, 'left')
        local this_block_top = redis.call('HGET', block_key, 'top')
        redis.call('DEL', block_key)
        if index == 1 then
            if direction == 'up' then
                redis.call('HSET', snake_key..':block:1', 'left', first_block_left, 'top', first_block_top - 20)
            elseif direction == 'down' then
                redis.call('HSET', snake_key..':block:1', 'left', first_block_left, 'top', first_block_top + 20)
            elseif direction == 'left' then
                redis.call('HSET', snake_key..':block:1', 'left', first_block_left - 20, 'top', first_block_top)
            elseif direction == 'right' then
                redis.call('HSET', snake_key..':block:1', 'left', first_block_left + 20, 'top', first_block_top)
            end
        else
            redis.call('HSET', snake_key..':block:'..get_block_number(block_key) + 1, 'left', this_block_left, 'top', this_block_top)
        end
    end
end
for _, snake in ipairs(snakes) do
    local snake_key = string.sub(snake,1, -11)

end
return redis.status_reply('OK')