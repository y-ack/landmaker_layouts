mainrom = manager.machine.memory.regions[":maincpu"]
function save_layout(addr,fname)
  local addr = mainrom:read_u32(addr)
  out = io.open(fname,"w")
  repeat
    -- space separated words?? do we like these??
    w = mainrom:read_u16(addr)
    out:write(string.format("%04X ",w))
    addr = addr + 2
  until w == 0xffff
  out:close()
  print("saved " .. fname)
end

-- 2.01
LAYOUTS_TUTORIAL = 0x9874E
LAYOUTS_NORMAL = 0x9878E
LAYOUTS_MYSTERY = 0x9888E
LAYOUTS_AW = 0x9892E
LAYOUTS_PRAC = 0x98A8E
LAYOUTS_PRAC_AW = 0x98AEE

for i = 0, 43, 1 do
  name = string.format("layout_norm_%d_%d",i // 4 + 1, i % 4 + 1)
  save_layout(LAYOUTS_NORMAL + i * 4 * 2, name)
  save_layout(LAYOUTS_NORMAL + i * 4 * 2 + 4, name .. "u")
end

for i = 0, 7, 1 do
  name = string.format("layout_teach_%d_%d",i // 4 + 1, i % 4 + 1)
  save_layout(LAYOUTS_TUTORIAL + i * 4 * 2, name)
  save_layout(LAYOUTS_TUTORIAL + i * 4 * 2 + 4, name .. "u")
end


for i = 0, 7, 1 do
  name = string.format("layout_mystery_%d_%d",i // 4 + 1, i % 4 + 1)
  save_layout(LAYOUTS_MYSTERY + i * 4 * 2, name)
  save_layout(LAYOUTS_MYSTERY + i * 4 * 2 + 4, name .. "u")
end

for i = 0, 43, 1 do
  name = string.format("layout_aw_%d_%d",i // 4 + 1, i % 4 + 1)
  save_layout(LAYOUTS_AW + i * 4 * 2, name)
  save_layout(LAYOUTS_AW + i * 4 * 2 + 4, name .. "u")
end

for i = 0, 11, 1 do
  name = string.format("layout_prac_%d_%d",i // 4 + 1, i % 4 + 1)
  save_layout(LAYOUTS_PRAC + i * 4 * 2, name)
  save_layout(LAYOUTS_PRAC + i * 4 * 2 + 4, name .. "u")
end

for i = 0, 11, 1 do
  name = string.format("layout_prac_aw_%d_%d",i // 4 + 1, i % 4 + 1)
  save_layout(LAYOUTS_PRAC_AW + i * 4 * 2, name)
  save_layout(LAYOUTS_PRAC_AW + i * 4 * 2 + 4, name .. "u")
end

