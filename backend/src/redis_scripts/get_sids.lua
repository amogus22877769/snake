local res = {}
local sids_keys = redis.call('KEYS', 'snake:*:sid')
for _, sid_key in ipairs(sids_keys) do
    table.insert(res, redis.call('GET', sid_key))
end
return res