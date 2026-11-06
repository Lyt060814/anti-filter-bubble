-- Pandoc filters for the PDF build.
-- 1. Rewrite relative repository links to GitHub URLs so they still work inside a standalone PDF.
-- 2. Drop the equal column widths pandoc derives from `|---|---|` rows, so the browser sizes columns by content.
-- The base directory of the source Markdown (relative to the repository root) is passed as
-- metadata `source-dir`, e.g. -M source-dir=docs/project-plan
local repo = "https://github.com/Lyt060814/anti-filter-bubble"
local base = "docs/project-plan"

local function normalise(path)
  local parts = {}
  for part in path:gmatch("[^/]+") do
    if part == ".." then
      table.remove(parts)
    elseif part ~= "." then
      table.insert(parts, part)
    end
  end
  return table.concat(parts, "/")
end

function Meta(meta)
  if meta["source-dir"] then
    base = pandoc.utils.stringify(meta["source-dir"])
  end
end

function Link(el)
  local t = el.target
  if t:match("^%a[%w+.-]*:") or t:match("^#") then
    return el
  end
  local path, anchor = t:match("^([^#]*)(#?.*)$")
  local full = normalise(base .. "/" .. path)
  local kind = path:sub(-1) == "/" and "tree" or "blob"
  el.target = repo .. "/" .. kind .. "/main/" .. full .. anchor
  return el
end

function Table(tbl)
  for i, spec in ipairs(tbl.colspecs) do
    tbl.colspecs[i] = {spec[1], pandoc.ColWidthDefault}
  end
  return tbl
end

return {{Meta = Meta}, {Link = Link, Table = Table}}
