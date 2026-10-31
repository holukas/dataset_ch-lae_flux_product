-- Used only by the PDF profile (_quarto-pdf.yml).
--
-- 1. Links. A link from one page to another (`L3.2.md#tests`), or to a notebook
--    or a dashboard (`notebooks/…html`, `dashboards/…html`), has no target inside
--    the PDF: the notebooks and dashboards are not in it, and the anchors of
--    different pages can share a name. Such links are pointed at the page on the
--    website instead (`<site>/L3.2.html#tests`). Links within a page (`#tests`),
--    links to other sites and mail links are left as they are.
--
-- 2. Lone `-` and `/`. Pandoc's Typst writer leaves a word that is only `-` or
--    `/` unescaped, and Typst reads it as list or term-list markup: the table
--    cell `- / E2` of the setup table stops the build ("expected colon"). Such
--    words are written as escaped Typst characters.
--
-- 3. Repeated heading ids. Every page is a chapter of one document in the PDF,
--    and Typst stops on a label that occurs twice; several pages have a
--    `## Known limitations {#known-limitations}`. From its second occurrence on,
--    an id gets the chapter number appended, and the links within that chapter
--    follow it.
--
-- 4. Table column widths. A pipe table with a long row gets relative column
--    widths from its dashes, and in Typst a narrow column then cannot hold a
--    raw file name such as `2004033014.b00`: the columns of the EC setup table
--    overlap; without widths, Typst makes all columns equal, with the same
--    result. Each column gets a width in proportion to its content: at least its
--    longest word, more for a column of running text.

local site_url = nil

local function absolute(target)
  if target:match('^#') or target:match('^%a[%w+.-]*:') then
    return nil
  end
  local path, anchor = target:match('^([^#]*)(#?.*)$')
  path = path:gsub('^%./', '')
  path = path:gsub('%.qmd$', '.html'):gsub('%.md$', '.html')
  return site_url .. path .. anchor
end

local markup = { ['-'] = true, ['/'] = true, ['+'] = true, ['='] = true }

return {
  {
    Meta = function(meta)
      site_url = pandoc.utils.stringify(meta['pdf-site-url'] or '')
      if site_url ~= '' and not site_url:match('/$') then
        site_url = site_url .. '/'
      end
    end,
  },
  {
    Link = function(link)
      if site_url == nil or site_url == '' then
        return nil
      end
      local new = absolute(link.target)
      if new then
        link.target = new
        return link
      end
    end,
    Str = function(s)
      if markup[s.text] and FORMAT:match('typst') then
        return pandoc.RawInline('typst', '\\' .. s.text)
      end
    end,
    Table = function(tbl)
      local n = #tbl.colspecs
      local longest, total, count = {}, {}, {}
      for i = 1, n do
        longest[i], total[i], count[i] = 3, 0, 0
      end
      local function measure(rows)
        for _, row in ipairs(rows) do
          for i, cell in ipairs(row.cells) do
            if i <= n then
              local text = pandoc.utils.stringify(cell.contents)
              for word in text:gmatch('%S+') do
                longest[i] = math.max(longest[i], utf8.len(word) or #word)
              end
              total[i] = total[i] + (utf8.len(text) or #text)
              count[i] = count[i] + 1
            end
          end
        end
      end
      measure(tbl.head.rows)
      for _, body in ipairs(tbl.bodies) do
        measure(body.body)
      end
      local weights, sum = {}, 0
      for i = 1, n do
        local mean = count[i] > 0 and total[i] / count[i] or 0
        weights[i] = math.max(longest[i], 0.6 * mean)
        sum = sum + weights[i]
      end
      for i, spec in ipairs(tbl.colspecs) do
        tbl.colspecs[i] = { spec[1], weights[i] / sum }
      end
      return tbl
    end,
  },
  {
    Pandoc = function(doc)
      -- Both passes walk the document in reading order; a level-1 heading,
      -- wherever it is nested, starts a chapter. Pandoc has already numbered
      -- repeated automatic ids (`known-limitations-3`), but not explicit ones
      -- (`{#known-limitations}`); the suffix added here, `-ch<n>`, cannot meet
      -- Pandoc's numbers.
      local seen, renames, ids = {}, {}, {}
      local chapter = 0
      -- First pass: per chapter, the ids to rename and the ids it ends up with.
      doc:walk({
        traverse = 'topdown',
        Header = function(h)
          if h.level == 1 then
            chapter = chapter + 1
            ids[chapter] = {}
          end
          local id = h.identifier
          if id ~= '' and chapter > 0 then
            if seen[id] then
              renames[chapter] = renames[chapter] or {}
              renames[chapter][id] = id .. '-ch' .. chapter
              id = renames[chapter][id]
            else
              seen[id] = true
            end
            table.insert(ids[chapter], id)
          end
        end,
      })
      -- The id a link `#x` in a chapter means: its own heading `x`, renamed
      -- here or by Pandoc (`x-3`), else the target unchanged.
      local function resolve(ch, id)
        local map = renames[ch]
        if map and map[id] then
          return map[id]
        end
        for _, own in ipairs(ids[ch] or {}) do
          if own == id then
            return id
          end
        end
        for _, own in ipairs(ids[ch] or {}) do
          if own:match('^' .. id:gsub('%p', '%%%0') .. '%-%d+$') then
            return own
          end
        end
        return id
      end
      -- Second pass: rename the headings and point the links of each chapter
      -- at its own headings.
      chapter = 0
      return doc:walk({
        traverse = 'topdown',
        Header = function(h)
          if h.level == 1 then
            chapter = chapter + 1
          end
          local map = renames[chapter]
          if map and map[h.identifier] then
            h.identifier = map[h.identifier]
            return h
          end
        end,
        Link = function(link)
          local id = link.target:match('^#(.+)$')
          if id and chapter > 0 then
            local new = resolve(chapter, id)
            if new ~= id then
              link.target = '#' .. new
              return link
            end
          end
        end,
      })
    end,
  },
}
