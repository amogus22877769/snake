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
local events = {}
local function delete_snake(block_key)
    local snake = string.sub(block_key, 7, -1)
    local snake_name = ''
    for i = 1, #snake do
        local c = string.sub(snake, i, i)
        if c == ':' then
            break
        end
        snake_name = snake_name..c
    end
    local snake_keys = redis.call('KEYS', 'snake:'..snake_name..':*')
    for _, snake_key in ipairs(snake_keys) do
        redis.call('DEL', snake_key)
    end
    table.insert(events, {
        type = 'deleted',
        value = snake_name,
    })
end
local snakes = redis.call('KEYS', 'snake:*:direction')
-- Move stage
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
-- Check deaths stage
local all_snakes_blocks_keys = redis.call('KEYS', 'snake:*:block:*')
local all_blocks = {}
for i, block_key in ipairs(all_snakes_blocks_keys) do
    all_blocks[i] = {
        left = redis.call('HGET', block_key, 'left'),
        top = redis.call('HGET', block_key, 'top'),
        key = block_key,
    }
end
local first_blocks = redis.call('KEYS', 'snake:*:block:1')
for _, first_block in ipairs(first_blocks) do
    local block_left = redis.call('HGET', first_block, 'left')
    local block_top = redis.call('HGET', first_block, 'top')
    for i=1, #all_blocks do
        if block_left == all_blocks[i]['left'] and block_top == all_blocks[i]['top'] and first_block == all_blocks[i]['key'] then
            delete_snake(first_block)
        end
    end
end
for _, event in ipairs(events) do
    debug_log('type: '..event['type']..', value: '..event['value'])
end

return cjson.encode(events)
