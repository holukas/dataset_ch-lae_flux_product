-- Used only by the PDF profile (_quarto-pdf.yml), after Quarto's own filters.
--
-- Quarto draws a Mermaid cell to a PNG for the PDF and gives the image its
-- natural size in inches: the meteo product chain comes out 70 in wide, the
-- post-processing chain 17 in tall. Such an image is scaled down, keeping its
-- proportions, to fit the text area of the page. The PNG keeps its pixels, so
-- the diagram can still be read by zooming in the PDF viewer.

-- Text area of an A4 page with the margins of _quarto-pdf.yml, less room for
-- the running header and the caption (inches).
local MAX_WIDTH = 6.5
local MAX_HEIGHT = 8.5

local function inches(value)
  local n = value and tonumber(value:match('^([%d.]+)in$'))
  return n
end

return {
  {
    Image = function(img)
      if not img.src:match('mermaid') then
        return nil
      end
      local w, h = inches(img.attributes.width), inches(img.attributes.height)
      if not (w and h) then
        img.attributes.width = '100%'
        img.attributes.height = nil
        return img
      end
      local scale = math.min(MAX_WIDTH / w, MAX_HEIGHT / h, 1)
      img.attributes.width = string.format('%.2fin', w * scale)
      img.attributes.height = string.format('%.2fin', h * scale)
      return img
    end,
  },
}
