-- ARGV[1] - random left position
-- ARGV[2] - random top position
local function debug_log(message)
    redis.call('RPUSH', 'lua:debug:logs', message)
end
local function has_value (tab, val)
    for _, value in ipairs(tab) do
        if value == val then
            return true
        end
    end

    return false
end
local random_left = ARGV[1]
local random_top = ARGV[2]

local apples = redis.call('KEYS', 'apple:*')
local apple_index = 0
for i=1,1000 do
    if not has_value(apples, 'apple:'..i) then
        redis.call('HSET', 'apple:'..i, 'left', random_left, 'top', random_top)
        apple_index = i
        break
    end
end

return apple_index