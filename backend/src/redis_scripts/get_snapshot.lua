local result = {
    snakes = {},
    apples = {},
}
local snakes = redis.call('KEYS', 'snake:*:direction')
for _, snake in ipairs(snakes) do
    local snake_key = string.sub(snake,1, -11)
    local blocks_keys = redis.call('KEYS', snake_key..':block:*')
    local blocks = {}
    for _, block_key in ipairs(blocks_keys) do
        table.insert(blocks, {
            left = redis.call('HGET', block_key, 'left'),
            top = redis.call('HGET', block_key, 'top')
        })
    end
    table.insert(result['snakes'], {
        name = string.sub(snake_key, 7, -1),
        blocks = blocks,
        direction = redis.call('GET', snake),
    })
end

local apple_keys = redis.call('KEYS', 'apple:*')
for _, apple_key in ipairs(apple_keys) do
    table.insert(result['apples'], {
        left = redis.call('HGET', apple_key, 'left'),
        top = redis.call('HGET', apple_key, 'top')
    })
end

return cjson.encode(result)